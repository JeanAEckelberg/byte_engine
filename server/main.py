from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from server.models.base import Base
from server.database import SessionLocal, engine
from server.crud import crud_submission
from server.models.run import Run
from server.models.submission_run_info import SubmissionRunInfo
from server.models.group_run import GroupRun
from server.models.team import Team
from server.models.team_type import TeamType
from server.models.submission import Submission
from server.models.turn_table import TurnTable
from server.models.university import University
from server.models.submission import Submission

from server.schemas.submission.submission_schema import SubmissionSchema
from server.schemas.submission.submission_w_team import SubmissionWTeam

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


@app.get('/get_submission/', response_model=SubmissionSchema)
def get_submission(submission: SubmissionWTeam, db: Session = Depends(get_db)):
    # Retrieves a list of submissions where the submission id and uuids match
    submission_list: list[Submission] | None = crud_submission.read_all_W_filter(
        db, submission_id=submission.submission_id, team_id_uuid=submission.team_id_uuid)

    if submission_list is None:
        raise HTTPException(status_code=404, detail="Submission not found!")

    return submission_list[0]  # returns a single SubmissionSchema to give the submission data to the user


@app.get('/get_submissions/{vid}', response_model=list[SubmissionSchema])
def get_submissions(vid: int, db: Session = Depends(get_db)):
    return crud_submission.read_all_by_team_id(db, vid)


# @app.get('/unis/', response_model=list[UniversityBase])
# def get_unis():
