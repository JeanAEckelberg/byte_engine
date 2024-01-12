import itertools
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import threading
import time
import schedule

from datetime import datetime
from queue import Queue
from sqlalchemy.exc import IntegrityError

from server.runner_utils import DB
from server import runner_utils
from server.crud import crud_tournament, crud_submission, crud_run, crud_submission_run_info, crud_turn, crud_university, crud_team_type
from server.models.submission import Submission
from server.models.tournament import Tournament
from server.schemas.run.run_base import RunBase
from server.schemas.submission_run_info.submission_run_info_base import SubmissionRunInfoBase
from server.schemas.team_type.team_type_base import TeamTypeBase
from server.schemas.tournament.tournament_base import TournamentBase
from server.schemas.turn.turn_base import TurnBase
from server.schemas.university.university_base import UniversityBase
from server.server_config import Config

# Config for loggers
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class ClientRunner:
    """
    This class is responsible for running submitted client bots against each other and getting the results from the
    games.
    """
    def __init__(self):
        """
        Class variables
        ---------------

            self.config: Creates an instance of the Config class in ``server_config.py``. That file stores values that
            are used by the client_runner and visualizer_runner. Use that file to change the values, and **DO NOT**
            change them in any other file.

            self.total_number_of_games: An int representing the number of games to run during a tournament

            self.number_of

            self.index_to_seed_id
        """
        self.config: Config = Config()


        self.total_number_of_games: int = -1

        # IE how many combinations of clients can you make
        self.number_of_unique_games: int = -1

        # Maps a seed_index to a database seed_id
        self.index_to_seed_id: dict[int, int] = {}

        # needs 6 queues for tasks to complete
        self.jobqueues: list[Queue] = [Queue(), Queue(), Queue(), Queue(), Queue(), Queue()]

        self.version: str = self.get_version_number()

        self.best_run_for_client: dict = {}
        self.runner_temp_dir: str = os.path.join(os.getcwd(), 'server', 'runner_temp')
        self.seed_path: str = os.path.join(self.runner_temp_dir, 'seeds')

        # Number of times a client runs against the opponents
        self.total_number_of_games_for_one_client: int = 0

        self.tournament: int | Tournament = -1

        # self.loop.run_in_executor(None, self.await_input)
        # self.loop.call_later(5, self.external_runner())
        (schedule.every(self.config.SLEEP_TIME_SECONDS_BETWEEN_RUNS)
         .seconds
         .until(self.config.END_DATETIME)
         .do(self.external_runner))
        (schedule.every()
         .day
         .at(self.config.END_DATETIME.split()[-1])
         .do(self.close_server))

        self.buffUpData()

        try:
            while 1:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("Ending runner due to Keyboard Interrupt")
        except Exception as e:
            logging.warning("Ending runner due to {0}".format(e))
        finally:
            self.close_server()

    def external_runner(self) -> None:
        print('running')
        self.best_run_for_client = {}
        with DB() as db:
            clients = crud_submission.get_latest_submission_for_each_team(db)

        # if less than 2 submissions are present, don't proceed
        if len(clients) < 2:
            return
        print('More than 2')
        # get the games as a list of client tuples
        # submission_id_list = list(map(lambda x: x["submission_id"], clients))
        games: list[tuple[Submission, Submission]] = self.return_team_parings(clients)
        self.total_number_of_games_for_one_client = self.count_number_of_game_appearances(games)
        self.tournament = self.insert_new_tournament()

        self.delete_turns()

        if not os.path.exists(self.runner_temp_dir):
            os.mkdir(self.runner_temp_dir)

        if not os.path.exists(self.seed_path):
            os.mkdir(self.seed_path)

        for index in range(self.config.NUMBER_OF_GAMES_AGAINST_SAME_TEAM):
            path: str = os.path.join(self.seed_path, str(index))
            os.mkdir(path)
            shutil.copy('launcher.pyz', path)
            self.run_runner(path, os.path.join(os.getcwd(), 'server', 'runners', 'generator'))
            with open(os.path.join(path, 'logs', 'game_map.json'), 'r') as fl:
                gameboard: dict = json.load(fl)
            self.index_to_seed_id[index] = gameboard['game_board']['seed']

        # then run them in parallel using their index as a unique identifier
        [self.jobqueues[i % 6].put((self.internal_runner, games[i], i)) for i in range(self.total_number_of_games)]
        threads: list[threading.Thread] = [
            threading.Thread(target=runner_utils.worker_main, args=(self.jobqueues[i],)) for i in range(6)]
        [t.start() for t in threads]
        [t.join() for t in threads if t.is_alive()]
        self.read_best_logs_and_insert()
        self.delete_runner_temp()
        self.update_tournament_finished()
        logging.info(
            f'Sleeping for {self.config.SLEEP_TIME_SECONDS_BETWEEN_RUNS} seconds')
        self.tournament = -1
        print('Job completed\n')

    def internal_runner(self, submission_tuple, index) -> None:
        """

        :param submission_tuple:
        :param index:
        :return:
        """
        score_for_each_submission: dict[int, int] = {}
        results = dict()

        # Run game
        # Create a folder for this client and seed
        end_path = os.path.join(self.runner_temp_dir, str(index))
        if not os.path.exists(end_path):
            os.mkdir(end_path)

        shutil.copy('launcher.pyz', end_path)

        # Write the clients into the folder
        for index_2, submission in enumerate(submission_tuple):
            # runner will run -fn argument, which makes the file name the file name
            # So we can grab the submission_id out of the results later
            with open(os.path.join(end_path, f'client_{index_2}_{submission.submission_id}.py'), 'x') as f:
                f.write(str(submission.file_txt, 'utf-8'))

        # Determine what seed this run needs based on it's serial index
        seed_index = index // self.number_of_unique_games
        logging.info(f'running run {index} for game ({submission_tuple[0].submission_id}, '
                        f'{submission_tuple[1].submission_id}) using seed index {seed_index}')

        # Copy the seed into the run folder
        if os.path.exists(os.path.join(self.seed_path, str(seed_index), 'logs', 'game_map.json')):
            os.mkdir(os.path.join(end_path, 'logs'))
            shutil.copyfile(os.path.join(self.seed_path, str(seed_index), 'logs', 'game_map.json'),
                            os.path.join(end_path, 'logs', 'game_map.json'))

        try:
            res = self.run_runner(end_path, os.path.join(os.getcwd(), 'server', 'runners', 'runner'))

            if os.path.exists(os.path.join(end_path, 'logs', 'results.json')):
                with open(os.path.join(end_path, 'logs', 'results.json'), 'r') as f:
                    results: dict = json.load(f)

        finally:
            player_sub_ids: list[int] = [int(x["file_name"].split("_")[-1]) for x in results['players']]
            run_id: int = self.insert_run(
                self.tournament.tournament_id,
                self.index_to_seed_id[seed_index],
                results)
            for i, result in enumerate(results["players"]):
                self.insert_submission_run_info(player_sub_ids[i], run_id, result["error"], i,
                                                result["avatar"]["score"])
                score_for_each_submission[player_sub_ids[i]] = result["avatar"]["score"]

            # don't store logs with non-eligible teams
            if any([not submission.team.team_type.eligible for submission in submission_tuple]):
                return

            # Update information in best run dict
            for submission in submission_tuple:
                if (score_for_each_submission[submission.submission_id] >
                        self.best_run_for_client.get(submission.submission_id, {'score': -2})['score']):
                    self.best_run_for_client[submission.submission_id] = {}
                    self.best_run_for_client[submission.submission_id]["log_path"] = os.path.join(end_path, 'logs')
                    self.best_run_for_client[submission.submission_id]["run_id"] = run_id
                    self.best_run_for_client[submission.submission_id]["score"] = score_for_each_submission[submission.submission_id]

    def run_runner(self, end_path, runner) -> bytes:
        """
        runs a script in the runner folder.
        end path is where the runner is located
        runner is the name of the script (no extension)
        """
        f = open(os.devnull, 'w')
        if platform.system() == 'Linux':
            shutil.copy(runner + '.sh', os.path.join(end_path, 'runner.sh'))
            p = subprocess.Popen(f'bash {os.path.join(end_path, "runner.sh")}', stdout=f,
                                 cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
            p.wait()
            return stdout
        else:
            # server/runner.bat
            shutil.copy(runner + '.bat', os.path.join(end_path, 'runner.bat'))
            p = subprocess.Popen(os.path.join(end_path, 'runner.bat'), stdout=f,
                                 cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
            p.wait()
            return stdout

    def get_version_number(self) -> str:
        """
        runs a script in the runner folder.
        end path is where the runner is located
        runner is the name of the script (no extension)
        """

        stdout = ""
        if platform.system() == 'Linux':
            p = subprocess.Popen(os.path.join('server', 'runners', 'version.sh'),
                                 stdout=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
        else:
            p = subprocess.Popen(
                os.path.join('server', 'runners', 'version.bat'), stdout=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
        return stdout.decode("utf-8").split('\n')[-1]

    def insert_new_tournament(self) -> Tournament:
        """
        Inserts a new tournament. Relates all the runs in this process together
        """

        with DB() as db:
            return crud_tournament.create(db, TournamentBase(tournament_id=0,
                                                             start_run=datetime.utcnow(),
                                                             launcher_version=self.get_version_number(),
                                                             runs_per_client=self.total_number_of_games_for_one_client,
                                                             is_finished=False))

    def insert_run(self, tournament_id: int, seed_id: int, results: dict) -> int:
        """
        Inserts a run into the DB
        """
        with DB() as db:
            return crud_run.create(db, RunBase(run_id=0,
                                               tournament_id=tournament_id,
                                               run_time=datetime.utcnow(),
                                               seed=seed_id,
                                               results=json.dumps(results).encode("utf-8"))).run_id

    def insert_submission_run_info(self, submission_id: int, run_id: int, error: str | None, player_num: int,
                                   points_awarded: int) -> None:
        """

        :param submission_id:
        :param run_id:
        :param error:
        :param player_num:
        :param points_awarded:
        :return: None
        """
        if error is None:
            error = ''

        with DB() as db:
            submission_run_info = crud_submission_run_info.create(
                db, SubmissionRunInfoBase(submission_run_info_id=0,
                                          submission_id=submission_id,
                                          run_id=run_id,
                                          error_txt=error,
                                          player_num=player_num,
                                          points_awarded=points_awarded))

    def delete_tournament_cascade(self, tournament_id: int) -> None:
        """
        Deletes the tournament by using the given id
        :param tournament_id:
        :return: None
        """
        with DB() as db:
            crud_tournament.delete(db, tournament_id)

    def read_best_logs_and_insert(self) -> None:
        for submission_id in self.best_run_for_client:
            path = self.best_run_for_client[submission_id]["log_path"]
            turn_logs: list[TurnBase] = []
            for file in os.listdir(path):
                if file in ['game_map.json', 'results.json', 'turn_logs.json']:
                    continue
                with open(os.path.join(path, file)) as fl:
                    turn_logs.append(TurnBase(turn_number=int(file[-9:-5]), run_id=self.best_run_for_client[
                        submission_id]["run_id"], turn_data=bytes(fl.read(), 'utf-8')))

            self.insert_logs(turn_logs)

    def insert_logs(self, logs: list[TurnBase]) -> None:
        """
        Inserts logs
        """
        try:
            with DB() as db:
                crud_turn.create_all(db, logs)

        # do nothing if fails to insert due to records already existing
        except IntegrityError:
            ...

    def close_server(self) -> None:
        if self.tournament != -1 and not self.tournament.is_finished:
            self.delete_tournament_cascade(self.tournament.tournament_id)
        else:
            logging.warning("Not deleting any tournaments")
        self.delete_runner_temp()
        schedule.clear()
        sys.exit(0)

    def delete_runner_temp(self) -> None:
        while True:
            try:
                if os.path.exists(self.runner_temp_dir):
                    shutil.rmtree(self.runner_temp_dir)
                break
            except PermissionError:
                continue

    def delete_turns(self) -> None:
        with DB() as db:
            crud_turn.delete_all(db)

    def return_team_parings(self, submissions: list[Submission]) -> list[tuple[Submission, Submission]]:
        # do not remove
        # noinspection PyTypeChecker
        fixtures: list[tuple[Submission, Submission]] = list(itertools.permutations(submissions, 2))
        
        temp: list[tuple[Submission, ...]]
        self.number_of_unique_games = len(fixtures)
        repeated = fixtures * self.config.NUMBER_OF_GAMES_AGAINST_SAME_TEAM
        self.total_number_of_games = len(repeated)
        return repeated

    def count_number_of_game_appearances(self, games: list[tuple[Submission, Submission]]) -> int:
        one_id: int = games[0][0].submission_id
        count: int = sum([1 for game_tuple in games
                          if game_tuple[0].submission_id == one_id
                          or game_tuple[1].submission_id == one_id])
        return count

    def update_tournament_finished(self) -> None:
        """
        Updates the tournament to have the finished bool be True
        :return:
        """
        self.tournament.is_finished = True
        with DB() as db:
            self.tournament = crud_tournament.update(db, self.tournament.tournament_id,
                                                     TournamentBase(**self.tournament.__dict__))

    def buffUpData(self) -> None:
        with DB() as db:
            try:
                crud_university.create(db, UniversityBase(
                    uni_id=1,
                    uni_name='NDSU'
                ))
                print('NDSU Added')
            except IntegrityError:
                print('NDSU Already Exists')

            try:
                crud_university.create(db, UniversityBase(
                    uni_id=2,
                    uni_name='MSUM'
                ))
                print('MSUM Added')
            except IntegrityError:
                print('MSUM Already Exists')

            try:
                crud_university.create(db, UniversityBase(
                    uni_id=3,
                    uni_name='UND'
                ))
                print('UND Added')
            except IntegrityError:
                print('UND Already Exists')

            try:
                crud_team_type.create(db, TeamTypeBase(
                    team_type_id=1,
                    team_type_name='Undergrad',
                    eligible=True
                ))
                print('Undergrad Added')
            except IntegrityError:
                print('Undergrad Already Exists')

            try:
                crud_team_type.create(db, TeamTypeBase(
                    team_type_id=2,
                    team_type_name='Graduate',
                    eligible=False
                ))
                print('Graduate Added')
            except IntegrityError:
                print('Graduate Already Exists')

            try:
                crud_team_type.create(db, TeamTypeBase(
                    team_type_id=3,
                    team_type_name='Alumni',
                    eligible=False
                ))
                print('Alumni Added')
            except IntegrityError:
                print('Alumni Already Exists')


if __name__ == "__main__":
    ClientRunner()
