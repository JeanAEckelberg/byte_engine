import uuid
from typing import Type

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, func

from server.models.submission import Submission
from server.schemas.submission.submission_w_team import SubmissionWTeam


def create(submission: SubmissionWTeam, db: Session) -> Submission:
    db_submission: Submission = Submission(**submission.model_dump(exclude={'submission_id'}))
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def read(db: Session, id: int, eager: bool = False) -> Submission | None:
    return (db.query(Submission)
            .filter(Submission.submission_id == id)
            .first() if not eager
            else db.query(Submission)
            .options(joinedload(Submission.submission_run_infos),
                     joinedload(Submission.team))
            .filter(Submission.submission_id == id)
            .first())


def read_all_by_team_id(db: Session, team_uuid: uuid, eager: bool = False) -> list[Type[Submission]]:
    return (db.query(Submission)
            .filter(Submission.team_uuid == team_uuid)
            .all() if not eager
            else db.query(Submission)
            .options(joinedload(Submission.submission_run_infos),
                     joinedload(Submission.team))
            .filter(Submission.team_uuid == team_uuid)
            .all())


def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [Submission]:
    return (db.query(Submission)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(Submission)
            .options(joinedload(Submission.submission_run_infos),
                     joinedload(Submission.team))
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, submission: SubmissionWTeam) -> Submission | None:
    db_submission: Submission | None = (db.query(Submission)
                                        .filter(and_(Submission.submission_id == id,
                                                     Submission.team_uuid == submission.team_id_uuid))
                                        .one_or_none())
    if db_submission is None:
        return

    for key, value in submission.model_dump().items():
        setattr(db_submission, key, value) if value is not None else None

    db.commit()
    db.refresh(db_submission)
    return db_submission


def delete(db: Session, id: int, submission: SubmissionWTeam) -> None:
    db_submission: Submission | None = (db.query(Submission)
                                        .filter(and_(Submission.submission_id == id,
                                                     Submission.team_uuid == submission.team_id_uuid))
                                        .one_or_none())
    if db_submission is None:
        return

    db.delete(db_submission)
    db.commit()


def get_latest_submission(db: Session):
    return (db.query(Submission)
    .filter(Submission.submission_id.in_(
        db.query(func.max(Submission.submission_id))
        .group_by(Submission.team_uuid))))
