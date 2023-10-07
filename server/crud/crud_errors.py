import uuid
from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import and_

from server.models.submission_run_info import SubmissionRunInfo
from server.schemas.errors_schema import ErrorsBase, ErrorsSchema


def create(db: Session, errors: ErrorsBase) -> SubmissionRunInfo:
    db_errors: SubmissionRunInfo = SubmissionRunInfo(**errors.model_dump(exclude={'errors_id'}))
    db.add(db_errors)
    db.commit()
    db.refresh(db_errors)
    return db_errors


def read(db: Session, id: int) -> SubmissionRunInfo | None:
    return (db.query(SubmissionRunInfo)
            .filter(SubmissionRunInfo.error_id == id)
            .first())


def read_all(db: Session) -> [SubmissionRunInfo]:
    return db.query(SubmissionRunInfo).all()


def read_all_W_filter(db: Session, **kwargs) -> [SubmissionRunInfo]:
    return (db.query(SubmissionRunInfo)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, errors: ErrorsBase) -> SubmissionRunInfo | None:
    db_errors: SubmissionRunInfo | None = (db.query(SubmissionRunInfo)
                                           .filter(SubmissionRunInfo.error_id == id)
                                           .one_or_none())
    if db_errors is None:
        return

    for key, value in errors.model_dump().items():
        setattr(db_errors, key, value) if value is not None else None

    db.commit()
    db.refresh(db_errors)
    return db_errors


def delete(db: Session, id: int, errors: ErrorsBase) -> None:
    db_errors: SubmissionRunInfo | None = (db.query(SubmissionRunInfo)
                                           .filter(SubmissionRunInfo.error_id == id)
                                           .one_or_none())
    if db_errors is None:
        return

    db.delete(db_errors)
    db.commit()
