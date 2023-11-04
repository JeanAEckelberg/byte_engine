from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from server.models.base import Base
from server.database import SessionLocal, engine
from server.crud import crud_submission, crud_team_type, crud_university, crud_team, crud_group_run, crud_run, \
    crud_group_teams
from server.models.run import Run
from server.models.submission_run_info import SubmissionRunInfo
from server.models.group_run import GroupRun
from server.models.team import Team
from server.models.team_type import TeamType
from server.models.submission import Submission
from server.models.turn_table import TurnTable
from server.models.university import University
from server.models.group_teams import GroupTeams
from server.models.submission import Submission

from server.schemas.group_run.group_run_base import GroupRunBase
from server.schemas.group_run.group_run_schema import GroupRunSchema
from server.schemas.run.run_base import RunBase
from server.schemas.run.run_schema import RunSchema
from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.submission.submission_schema import SubmissionSchema
from server.schemas.submission.submission_w_team import SubmissionWTeam
from server.schemas.team.team_base import TeamBase
from server.schemas.team.team_schema import TeamSchema
from server.schemas.team_type.team_type_base import TeamTypeBase
from server.schemas.team_type.team_type_schema import TeamTypeSchema
from server.schemas.university.university_base import UniversityBase
from server.schemas.university.university_schema import UniversitySchema

Base().metadata.create_all(bind=engine)

# run in byte_engine folder: uvicorn server.main:app --reload
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API

@app.get('/')
def root():
    return {"message": "Hello World"}


# post submission
@app.post('/submission/', response_model=SubmissionBase)
def post_submission(submission: SubmissionWTeam, db: Session = Depends(get_db)):
    return crud_submission.create(db, submission)


# post team
@app.post('/team/', response_model=TeamBase)
def post_team(team: TeamSchema, db: Session = Depends(get_db)):
    return crud_team.create(db, team)


# gets the INDIVIDUAL submission data of a specific team
@app.get('/get_submission/{submission_id}/{team_uuid}', response_model=SubmissionSchema)
def get_submission(submission_id: int, team_uuid: int, db: Session = Depends(get_db)):
    # Retrieves a list of submissions where the submission id and uuids match
    submission_list: list[Submission] | None = crud_submission.read_all_W_filter(
        db, submission_id=submission_id, team_uuid=team_uuid)
    print('get_submission print')

    if submission_list is None:
        raise HTTPException(status_code=404, detail="Submission not found!")

    return submission_list[0]  # returns a single SubmissionSchema to give the submission data to the user


# gets MULTIPLE submission
# team_id = {vid}
@app.get('/get_submissions/{vid}', response_model=list[SubmissionSchema])
def get_submissions(vid: int, db: Session = Depends(get_db)):
    return crud_submission.read_all_by_team_id(db, vid)


# get team types
@app.get('/team_types/', response_model=list[TeamTypeBase])
def get_team_types(db: Session = Depends(get_db)):
    return crud_team_type.read_all(db)


# get universities
@app.get('/universities/', response_model=list[UniversityBase])
def get_universities(db: Session = Depends(get_db)):
    return crud_university.read_all(db)


# get group runs based off team uuid
@app.get('/group_runs/{team_uuid}', response_model=list[GroupRunBase])
def get_group_runs(team_uuid: str, db: Session = Depends(get_db)):
    group_team: GroupTeams
    return [group_team.group_run for group_team in crud_group_teams.read_all_W_filter(db, team_uuid=team_uuid)]


# get teams score over time, need team uuid
@app.get('/score_over_time/', response_model=list[GroupRunBase])
def get_score_over_time(group_run: GroupRunBase, db: Session = Depends(get_db)):
    group_run_list: list[Run] | None = crud_group_run.read_all_W_filter(
        db, group_run_id=group_run.group_run_id, team_uuid=group_run.team_uuid)

    if group_run_list is None:
        raise HTTPException(status_code=404, detail="not found")

    return group_run_list[0]


# get leaderboards - group_id, join team, submissions, run, university, pass-team_type
@app.get('/leaderboard/', response_model=list[GroupRunSchema])
def leaderboard(db: Session = Depends(get_db)):
    return crud_group_run.read_all(db)

# main should not be able to delete (we do not want the public to be able to delete)
# so we are not making a delete group runs endpoint
