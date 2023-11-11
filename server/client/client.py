import os
from requests.models import HTTPError
from server.client.client_utils import ClientUtils
import json

CLIENT_DIRECTORY = "./"
CLIENT_KEYWORD = "client"


class Client:
    def __init__(self, args):

        # If vID exists, read it
        if os.path.isfile('vID'):
            with open('vID') as f:
                self.vid = f.read()

        self.utils = ClientUtils(args.csv)
        self.handle_client(args)

    # Determines what action the client wants to do

    def handle_client(self, args):
        try:
            # If the subparse is None, don't attempt to do the rest of the code
            if args.subparse is None:
                print("The server command needs more information. Try 'python launcher.pyz s -h' for help")
                return

            # If the subparse doesn't contain an expected value, don't do anything
            if not args.subparse.lower() == 'stats' and not args.subparse.lower() == 's':
                return

            if args.subparse.lower() == 'leaderboard' or args.subparse.lower() == "l":
                return

            # The rest of the if statements will attempt to fulfill the desired command
            if args.register:
                self.register()
                return

            if args.submit:
                self.submit()
                return

            # need guard clause of the -1 in the client utils. Tell Julia
            self.utils.get_team_runs_for_group_run(self.vid, args.runs_for_group_run)

            if args.runs_for_submission != -1:
                self.utils.get_runs_for_submission(self.vid, args.runs_for_submission)
                return

            if args.get_submissions:
                self.utils.get_submissions(self.vid)
                return

            if args.get_group_runs:
                self.utils.get_group_runs(self.vid)
                return

            if args.get_code_for_submission != -1:
                self.utils.get_code_from_submission(self.vid, args.get_code_for_submission)
                return

            if args.subparse.lower() == 'get_seed' or args.subparse.lower() == 'gs':
                self.utils.get_seed_for_run(self.vid, args.run_id)
                return

            if args.get_errors_for_submission != -1:
                self.utils.get_errors_for_submission(self.vid, args.get_errors_for_submission)
                return
            else:
                self.get_submission_stats()

            if args.over_time:
                self.utils.get_team_score_over_time(self.vid)
                return
            else:
                self.utils.get_leaderboard(args.include_alumni, args.group_id)

        except HTTPError as e:
            print(f"Error: {json.loads(e.response._content)['error']}")

    def register(self):
        # Check if vID already exists and cancel out
        if os.path.isfile('vID'):
            print('You have already registered.')
            return

        # Ask for teamname
        teamname = input("Enter your teamname: ")

        if teamname == '':
            print("Teamname can't be empty.")
            return

        unis = self.utils.get_unis()

        print("Select a university (id)")
        self.utils.to_table(unis)

        uni_id = int(input())

        if uni_id not in map(lambda x: x['uni_id'], unis):
            print("Not a valid uni id")
            return

        team_types = self.utils.get_team_types()

        print("Select a team type (id)")
        self.utils.to_table(team_types)

        team_type = int(input())

        if team_type not in map(lambda x: x['team_type_id'], team_types):
            print("Not a valid team type")
            return

        response = self.utils.register(
            {"type": team_type, "uni": uni_id, "name": teamname})

        if not response.ok:
            print('Teamname contains illegal characters or is already taken.')
            return

        # Receive uuid
        # vID = await self.reader.read(BUFFER_SIZE)
        # vID = vID.decode()

        v_id = response.content
        if v_id == '':
            print('Something broke.')
            return

        # Put uuid into file for verification (vID)
        with open('vID', 'w+') as f:
            f.write(v_id.decode('UTF-8'))

        print("Registration successful.")
        print("You have been given an ID file in your Byte-le folder. Don't move or lose it!")
        print("You can give a copy to your teammates so they can submit and view stats.")

    def submit(self):
        if not self.verify():
            print('You need to register first.')
            return

        # Check and verify client file
        file = None
        for filename in os.listdir(CLIENT_DIRECTORY):
            if CLIENT_KEYWORD.upper() not in filename.upper():
                # Filters out files that do not contain CLIENT_KEYWORD in their filename
                continue

            if os.path.isdir(os.path.join(CLIENT_DIRECTORY, filename)):
                # Skips folders
                continue

            user_check = input(f'Submitting {filename}, is this ok? (y/n): ')
            if 'y' in user_check.lower():
                file = filename
                break
        else:
            file = input(
                'Could not find file: please manually type file name: ')

        if not os.path.isfile(CLIENT_DIRECTORY + file):
            print('File not found.')
            return

        # Send client file
        print('Submitting file.')
        with open(CLIENT_DIRECTORY + file) as fl:
            fil = "".join(fl.readlines())
            self.utils.submit_file(fil, self.vid)

        print('File sent successfully.')

    def get_submission_stats(self):
        res = self.utils.get_submission_stats(self.vid)
        print("Current Submission stats for submission {0} in group run {1}".format(res["sub_id"], res["run_group_id"]))
        print(f"Your submission has been run {len(res['data'])} out of {res['runs_per_client']} times")
        self.utils.to_table(res["data"])

    def verify(self):
        # Check vID for uuid
        if not os.path.isfile('vID'):
            print("Cannot find vID, please register first.")
            return False
        return True
