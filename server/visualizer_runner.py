import datetime
import sys
import time
import json
import os
import shutil
import subprocess
import schedule

from server.crud import crud_tournament
from server.database import SessionLocal
from server.models.run import Run
from server.models.tournament import Tournament
from server.models.turn import Turn
from server.server_config import Config


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class visualizer_runner:
    def __init__(self):

        # Current tournament id of logs
        self.tournament_id: int = 0

        self.logs_path: str = 'server/vis_temp'

        try:
            while 1:
                schedule.run_pending()
                time.sleep(1)
        except (KeyboardInterrupt, Exception) as e:
            print(f'Ending visualizer due to {e}')

    # Get new logs from the latest tournament
    @schedule.repeat(schedule.every(Config().SLEEP_TIME_SECONDS_BETWEEN_VIS).seconds.until(Config().END_DATETIME))
    def internal_runner(self) -> None:
        tournament: Tournament | None = self.get_latest_tournament()
        if self.tournament_id != tournament.tournament_id:
            print("Getting new logs")
            self.get_latest_log_files(tournament)
            self.tournament_id = tournament.tournament_id
        self.visualizer_loop()

    # Delete visual logs path at end of competition
    @schedule.repeat(schedule.every().day.at(Config().END_DATETIME))
    def delete_vis_temp(self) -> None:
        if not os.path.exists(self.logs_path):
            os.mkdir(self.logs_path)
        else:
            shutil.rmtree(self.logs_path)
            os.mkdir(self.logs_path)

    def get_latest_log_files(self, tournament: Tournament) -> None:
        self.delete_vis_temp()

        print("Getting latest log files")
        run: Run
        logs: list[list[Turn]] = [run.turns for run in tournament.runs if len(run.turns) > 0]

        log: list[Turn]
        for log in logs:
            # Take logs and copy into directory
            id_dir = f'{self.logs_path}/{log[0].run_id}'
            os.mkdir(id_dir)
            logs_dir = id_dir + "/logs"
            os.mkdir(logs_dir)
            for turn in log:
                with open(f"{logs_dir}/{f'turn_{turn.turn_number:04d}.json'}", "w") as fl:
                    fl.write(turn.turn_data)

            shutil.copy('launcher.pyz', id_dir)
            shutil.copy('server/runners/vis_runner.sh', id_dir)
            shutil.copy('server/runners/vis_runner.bat', id_dir)
            shutil.copytree('Visualiser', id_dir + '/Visualiser')

    def get_latest_tournament(self) -> Tournament | None:
        print("Getting Latest Tournament")
        with get_db() as db:
            return crud_tournament.get_latest_tournament(db) if not None else None

    def visualizer_loop(self) -> None:
        try:
            f = open(os.devnull, 'w')
            for id in os.listdir(self.logs_path):
                idpath = f"{self.logs_path}/{id}"

                p = subprocess.Popen('bash vis_runner.sh', stdout=f, cwd=idpath, shell=True) \
                    if sys.platform != 'win32' \
                    else subprocess.Popen('vis_runner.bat', stdout=f, cwd=idpath, shell=True)

                stdout, stderr = p.communicate()

        except PermissionError:
            print("Whoops")


if __name__ == "__main__":
    visualizer_runner()
