import requests
import json
import urllib3
import os
from datetime import datetime, timezone, tzinfo


class ClientUtils:
    def __init__(self, csv_bool):
        urllib3.disable_warnings()
        self.IP = 'http://134.129.91.211:8000/api/'
        self.PORT = 8000
        self.path_to_public = False
        self.use_csv = csv_bool

    # convert utc to local time
    def convert_utc_to_local(self, utc_str: str = '2000-10-31T06:30:00Z') -> datetime:
        a: datetime = datetime.strptime(utc_str, '%Y-%m-%dT%H:%M:%SZ')
        tz: tzinfo = datetime.now().astimezone().tzinfo
        a = a.replace(tzinfo=timezone.utc)

        return a.astimezone(tz)

    # get team types
    def team_types(self):
        resp = requests.get(self.IP + "team_types",
                            verify=self.path_to_public)
        resp.raise_for_status()
        return json.loads(resp.content)

    # get unis
    def get_unis(self):
        resp = requests.get(self.IP + "universities", verify=self.path_to_public)
        resp.raise_for_status()
        return json.loads(resp.content)

    # post leaderboard
    def get_leaderboard(self, include_inelligible, group_run_id):
        data = {"include_inelligible": include_inelligible, "group_run_id": group_run_id}
        resp = requests.post(self.IP + "leaderboard",
                             json=data, verify=self.path_to_public)
        resp.raise_for_status()
        jsn = json.loads(resp.content)
        group_info = jsn['group_run_info']
        if not include_inelligible:
            print(
                f"The following is the leaderboard for eligible contestants for group run {group_info['group_run_id']}.")
        else:
            print(
                f"The following is the leaderboard for all contestants for group run {group_info['group_run_id']}.")
        print(
            f"""This group run ran with the launcher version {group_info['launcher_version']} on {group_info['start_run']}. Each client was run {group_info['runs_per_client']} times.""")
        self.to_table(jsn["data"])

    # def to_leaderboard_record(self, group_runs: list[dict]):
    #
    #     to_return: dict = {
    #         "Team Name": group_runs
    #     }


    # post get score over time - fix later
    def get_score_over_time(self, vid, group_run_id, team_uuid):
        resp = requests.post(
            self.IP + "get_score_over_time", json={"vid": vid}, verify=self.path_to_public)
        resp.raise_for_status()
        jsn = json.loads(resp.content)
        print("The following is your team's performance in each group run")
        self.to_table(jsn)

    # post submission
    def get_submission_stats(self, vid):
        resp = requests.post(
            self.IP + "submission", json={"vid": vid}, verify=self.path_to_public)
        resp.raise_for_status()
        return json.loads(resp.content)

    # gets the runs from a INDIVIDUAL get_submission
    def get_submission(self, vid, subid, teamuuid):
        resp = requests.get(
            self.IP + "get_submission", json={"vid": vid, "submissionid": subid, 'teamuuid': teamuuid},
            verify=self.path_to_public)
        resp.raise_for_status()
        jsn = json.loads(resp.content)
        jsn['submission_time'] = self.convert_utc_to_local(utc_str=jsn['submission_time']).strftime(
            "%m/%d/%Y, %H:%M:%S")
        self.to_table(jsn)

    # MULTIPLE get_submissions
    def get_submissions(self, vid):
        resp = requests.post(
            self.IP + f"get_submissions/{vid}", verify=self.path_to_public)
        resp.raise_for_status()
        jsn = json.loads(resp.content)
        jsn['submission_time'] = self.convert_utc_to_local(utc_str=jsn['submission_time']).strftime(
            "%m/%d/%Y, %H:%M:%S")
        self.to_table(jsn)

    # get group_runs
    def get_group_runs(self, vid):
        resp = requests.get(
            self.IP + f"group_runs/{vid}", verify=self.path_to_public)
        resp.raise_for_status()
        jsn = json.loads(resp.content)
        jsn['start_run'] = self.convert_utc_to_local(utc_str=jsn['start_run']).strftime("%m/%d/%Y, %H:%M:%S")
        self.to_table(jsn)

    # post team
    def team(self, vid):
        resp = requests.post(
            self.IP + "team", json={"vid": vid}, verify=self.path_to_public)
        resp.raise_for_status()
        return json.loads(resp.content)

    # get run
    def run(self, vid: int):
        resp = requests.get(self.IP + f'run/{vid}', verify=self.path_to_public)
        resp.raise_for_status()
        return json.loads(resp.content)

    # get get_run
    def get_run(self, teamuuid: str, vid: int, runid, group_run_id):
        resp = requests.get(self.IP + f'get_run',
                            json={'vid': vid, 'runid': runid, 'teamuuid': teamuuid, 'group_run_id': group_run_id},
                            verify=self.path_to_public)
        resp.raise_for_status()
        jsn = json.loads(resp.content)
        jsn['run_time'] = self.convert_utc_to_local(utc_str=jsn['run_time']).strftime("%m/%d/%Y, %H:%M:%S")
        self.to_table(jsn)

    # Building a comma-separated-values list table or ascii table based on passed in data below
    # The tables are used to build the leaderboard

    # helper method to format the csv or ascii table
    def get_longest_cell_in_cols(self, json, json_atribs):
        col_longest_length = {}
        for key in json_atribs:
            col_longest_length[key] = (len(key))
        for col in json_atribs:
            for row in json:
                if len(str(row[col])) > col_longest_length[col]:
                    col_longest_length[col] = len(str(row[col]))
        return col_longest_length

    # creates a line that separates rows of information in the table
    def get_seperator_line(self, col_longest_length, padding):
        rtn = ""
        for key in col_longest_length:
            rtn += "+" + ("-" * (col_longest_length[key] + padding))
        return rtn + "+"

    # prints table based on passed bool on instantiation
    def to_table(self, json):
        if self.use_csv:
            self.to_csv_table(json)
        else:
            self.to_ascii_table(json)

    # prints the csv table
    def to_csv_table(self, json):
        try:
            padding = 4
            json_atribs = json[0].keys()
            output = ""
            for index, key in enumerate(json_atribs):
                output += key
                if index != len(json_atribs) - 1:
                    output += ","
            output += "\n"
            for row in json:
                for index, col in enumerate(row):
                    if isinstance(row[col], int) or isinstance(row[col], float):
                        output += str(row[col])
                    else:
                        output += '"' + str(row[col]) + '"'
                    if index != len(row) - 1:
                        output += ","
                output += "\n"
            print(output)
        except BaseException as e:
            print(e)
            print(
                "Something went wrong. Maybe there isn't data for what you're looking for")

    # prints the ascii table
    def to_ascii_table(self, json):
        try:
            padding = 4
            json_atribs = json[0].keys()
            col_longest_length = self.get_longest_cell_in_cols(
                json, json_atribs)
            line_seperator = self.get_seperator_line(
                col_longest_length, padding)
            row_format = ""
            for key in json_atribs:
                row_format += "|{:^" + \
                              str(col_longest_length[key] + padding) + "}"
            row_format += "|"
            print(line_seperator)
            print(row_format.format(*json_atribs))
            for row in json:
                print(line_seperator)
                print(row_format.format(*[str(x) for x in row.values()]))
            print(line_seperator)
        except BaseException as e:
            print(e)
            print(
                "Something went wrong. Maybe there isn't data for what you're looking for")
