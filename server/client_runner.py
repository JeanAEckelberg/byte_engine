from datetime import datetime
import itertools
import json
import logging
import os
import platform
import random
import shutil
import subprocess
import sys
import threading
import time
from queue import Queue

import schedule

from server import runner_utils
from server.crud import crud_tournament, crud_submission, crud_run, crud_submission_run_info, crud_turn
from server.database import SessionLocal
from server.schemas.run.run_base import RunBase
from server.models.run import Run
from server.schemas.submission_run_info.submission_run_info_base import SubmissionRunInfoBase
from server.models.submission import Submission
from server.schemas.tournament.tournament_base import TournamentBase
from server.models.tournament import Tournament
from server.schemas.turn.turn_base import TurnBase
from server.server_config import Config

# Config for loggers
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ClientRunner:
    def __init__(self):
        self.config: Config = Config()
        # The group run ID. will be
        # set by insert_new_group_runlauncher.pyz

        self.total_number_of_games: int = -1

        # IE how many combinations of clients can you make
        self.number_of_unique_games: int = -1

        # Maps a seed_index to a database seed_id
        self.index_to_seed_id: dict[int, int] = {}

        # needs 6 queues for tasks to complete
        self.jobqueues: list[Queue] = [Queue(), Queue(), Queue(), Queue(), Queue(), Queue()]

        self.version: str = self.get_version_number()

        self.best_run_for_client = {}
        self.runner_temp_dir: str = 'server/runner_temp'
        self.seed_path: str = f"{self.runner_temp_dir}/seeds"

        # Number of times a client runs against the opponents
        self.total_number_of_games_for_one_client: int = 0

        self.tournament: int | Tournament = -1

        # self.loop.run_in_executor(None, self.await_input)
        # self.loop.call_later(5, self.external_runner())
        try:
            while 1:
                schedule.run_pending()
                time.sleep(1)

        except (KeyboardInterrupt, Exception) as e:
            logging.warning("Ending runner due to {0}".format(e))
        finally:
            self.close_server()

    @schedule.repeat(schedule.every(Config().SLEEP_TIME_SECONDS_BETWEEN_RUNS).seconds.until(Config().END_DATETIME))
    def external_runner(self) -> None:
        self.best_run_for_client = {}
        with get_db() as db:
            clients = crud_submission.get_latest_submission_for_each_team(db)

        # if less than 2 submissions are present, don't proceed
        if len(clients) < 2:
            return

        # get the games as a list of client tuples
        # submission_id_list = list(map(lambda x: x["submission_id"], clients))
        games: list[tuple[Submission, Submission]] = self.return_team_parings(clients)
        self.total_number_of_games_for_one_client = self.count_number_of_game_appearances(games)
        self.tournament = self.insert_new_tournament()

        if not os.path.exists(self.runner_temp_dir):
            os.mkdir(self.runner_temp_dir)

        if not os.path.exists(self.seed_path):
            os.mkdir(self.seed_path)

        for index in range(self.config.NUMBER_OF_GAMES_AGAINST_SAME_TEAM):
            path: str = f'{self.seed_path}/{index}'
            os.mkdir(path)
            shutil.copy('launcher.pyz', path)
            self.run_runner(path, "server/runners/generator")
            with open(f'{path}/logs/game_map.json') as fl:
                gameboard: dict = json.load(fl)
            self.index_to_seed_id[index] = gameboard['seed']

        # then run them in parallel using their index as a unique identifier
        [self.jobqueues[i % 6].put(self.internal_runner(games[i], i)) for i in range(self.total_number_of_games)]
        threads: list[threading.Thread] = [
            threading.Thread(target=runner_utils.worker_main, args=(self.jobqueues[i],)) for i in range(6)]
        [t.join() for t in threads]
        self.read_best_logs_and_insert()
        self.delete_runner_temp()
        self.update_tournament_finished()
        logging.warning(
            f"Sleeping for {self.config.SLEEP_TIME_SECONDS_BETWEEN_RUNS} seconds")
        self.tournament = -1

    # WILL NEED TO BE MODIFIED: INTERNAL RUNNER
    def internal_runner(self, submission_tuple, index) -> None:
        winner = -1
        max_score: int = -1
        errors = {}
        results = dict()
        try:
            # Run game
            # Create a folder for this client and seed
            end_path = f'{self.runner_temp_dir}/{index}'
            if not os.path.exists(end_path):
                os.mkdir(end_path)

            shutil.copy('launcher.pyz', end_path)

            # Write the clients into the folder
            for index_2, submission in enumerate(submission_tuple):
                # runner will run -fn argument, which makes the team name the file name
                # So we can grab the submission_id out of the results later
                with open(f"{end_path}/client_{index_2}_{submission.submission_id}.py", 'w') as f:
                    f.write(submission.file_txt)
                index_2 += 1

            # Determine what seed this run needs based on it's serial index
            seed_index = index // self.number_of_unique_games
            logging.warning(f'running run {index} for game ({submission_tuple[0].submission_id}, '
                            f'{submission_tuple[1].submission_id}) using seed index {seed_index}')

            # Copy the seed into the run folder
            if os.path.exists(f"{self.seed_path}/{seed_index}/logs/game_map.json"):
                os.mkdir(f"{end_path}/logs")
                shutil.copyfile(
                    f"{self.seed_path}/{seed_index}/logs/game_map.json", f"{end_path}/logs/game_map.json")

            res = self.run_runner(end_path, "server/runners/runner")

            if os.path.exists(end_path + '/logs/results.json'):
                with open(end_path + '/logs/results.json', 'r') as f:
                    results: dict = json.load(f)

            # BIG FIX IT
            # CHANGE THIS LINE TO GET CORRECT SCORE FOR GAME

        finally:

            player_sub_ids = [x["file_name"].split("_")[-1] for x in results["players"]]
            # FIX IT BEFORE I FIX YOU
            run_id: int = self.insert_run(
                self.tournament.tournament_id,
                self.index_to_seed_id[seed_index],
                results)
            for i, result in enumerate(results["players"]):
                self.insert_submission_run_info(player_sub_ids[i], run_id, result["error"], i,
                                                result["avatar"]["score"])

            # CURRENT IMPLEMENTATION OF BEST RUN FOR CLIENT MUST BE MODIFIED FOR NEW SYSTEM
            # FIGURE IT OUT
            # Update information in best run dict
            for submission in submission_tuple:
                if max_score > self.best_run_for_client.get(submission.submission_id, {'score': -2})["score"]:
                    self.best_run_for_client[submission.submission_id] = {}
                    self.best_run_for_client[submission.submission_id]["log_path"] = end_path + "/logs"
                    self.best_run_for_client[submission.submission_id]["run_id"] = run_id
                    self.best_run_for_client[submission.submission_id]["score"] = max_score

    def run_runner(self, end_path, runner) -> bytes:
        """
        runs a script in the runner folder.
        end path is where the runner is located
        runner is the name of the script (no extension)
        """
        f = open(os.devnull, 'w')
        if platform.system() == 'Linux':
            shutil.copy(runner + '.sh', f"{end_path}/runner.sh")
            p = subprocess.Popen('bash runner.sh', stdout=f,
                                 cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
            return stdout
        else:
            # server/runner.bat
            shutil.copy(runner + '.bat', f"{end_path}/runner.bat")
            p = subprocess.Popen('runner.bat', stdout=f,
                                 cwd=end_path, shell=True)
            stdout, stderr = p.communicate()
            return stdout

    def get_version_number(self) -> str:
        """
        runs a script in the runner folder.
        end path is where the runner is located
        runner is the name of the script (no extension)
        """

        stdout = ""
        if platform.system() == 'Linux':
            p = subprocess.Popen('server/runners/version.sh',
                                 stdout=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
        else:
            p = subprocess.Popen(
                'runner.bat', stdout=subprocess.PIPE, shell=True)
            stdout, stderr = p.communicate()
        return stdout.decode("utf-8")

    def insert_new_tournament(self) -> Tournament:
        """
        Inserts a new tournament. Relates all the runs in this process together
        """

        with get_db() as db:
            return crud_tournament.create(db, TournamentBase())

    def insert_run(self, tournament_id: int, seed_id: int, results: dict) -> int:
        """
        Inserts a run into the DB
        """
        with get_db() as db:
            return crud_run.create(db, RunBase(run_id=0,
                                               tournament_id=tournament_id,
                                               run_time=datetime.now(),
                                               seed_id=seed_id,
                                               results=bytes(str(results), "utf-8"))).run_id

    def insert_submission_run_info(self, submission_id: int, run_id: int, error: str | None, player_num: int,
                                   points_awarded: int) -> None:
        """
        Inserts a run into the DB
        """
        with get_db() as db:
            submission_run_info = crud_submission_run_info.create(db, SubmissionRunInfoBase(submission_run_info_id=0,
                                                                                            submission_id=submission_id,
                                                                                            run_id=run_id,
                                                                                            error=error,
                                                                                            player_num=player_num,
                                                                                            points_awarded=points_awarded))

    def delete_tournament_cascade(self, tournament_id) -> None:
        """
        Deletes the tournament by using the given id
        """
        with get_db() as db:
            crud_tournament.delete(db, tournament_id)

    def read_best_logs_and_insert(self) -> None:
        for submission_id in self.best_run_for_client:
            path = self.best_run_for_client[submission_id]["log_path"]
            turn_logs: list[TurnBase] = []
            for file in os.listdir(path):
                with open(f"{path}/{file}") as fl:
                    # It would probably be better to store each file in its own row
                    # But I'm lazy, and I'm just going to denote the split with the delimiter below
                    turn_logs.append(TurnBase(turn_id=0, turn_number=file[-4:], run_id=self.best_run_for_client[
                        submission_id]["run_id"], turn_data=fl.read()))

            self.insert_logs(turn_logs)

    def insert_logs(self, logs: list[TurnBase]) -> None:
        """
        Inserts logs
        """
        with get_db() as db:
            crud_turn.create_all(db, logs)

    @schedule.repeat(schedule.every().day.at(Config().END_DATETIME.split()[:-1]))
    def close_server(self) -> None:
        if self.tournament.tournament_id != -1:
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

    def return_team_parings(self, submissions: list[Submission]) -> list[tuple[Submission, Submission]]:
        fixtures = list(itertools.permutations(submissions, 2))
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
        with get_db() as db:
            self.tournament = crud_tournament.update(db, self.tournament.tournament_id,
                                                     TournamentBase(**self.tournament.__dict__))


if __name__ == "__main__":
    ClientRunner().external_runner()
