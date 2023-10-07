from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models.base import Base
from database import SessionLocal, engine
from crud import crud_errors, crud_submission
from models.run import Run
from models.errors import Errors
from models.group_run import GroupRun
from models.team import Team
from models.team_type import TeamType
from models.submission import Submission
from models.turn_table import TurnTable
from models.university import University
from schemas.university_schema import *
from schemas.submission_schema import *
from schemas.errors_schema import *

Base.metadata.create_all(bind=engine)

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


@app.get('/get_errors_for_submission', response_model=list[ErrorsBase])
def get_errors_for_submission(submission: SubmissionWTeam, db: Session = Depends(get_db)):
    # Retrieves a list of submissions where the submission id and uuids match
    submission_list: list[Submission] | None = crud_submission.read_all_W_filter(
        db, submission_id=submission.submission_id, team_id_uuid=submission.team_id_uuid)

    if submission_list is None:
        raise HTTPException(status_code=404, detail="Submission not found!")

    return submission_list[0].errors

# @app.get('/')


# @app.get('/unis/', response_model=list[UniversityBase])
# def get_unis():
