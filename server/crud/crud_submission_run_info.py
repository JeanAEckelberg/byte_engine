from sqlalchemy.orm import Session

from server.models.submission_run_info import SubmissionRunInfo
from server.schemas.submission_run_info.submission_run_info_schema import SubmissionRunInfoBase


def create(db: Session, submission_run_info: SubmissionRunInfoBase) -> SubmissionRunInfo:
    db_submission_run_info: SubmissionRunInfo = SubmissionRunInfo(**submission_run_info.model_dump(
        exclude={'submission_run_info_id'}))
    db.add(db_submission_run_info)
    db.commit()
    db.refresh(db_submission_run_info)
    return db_submission_run_info


def read(db: Session, id: int) -> SubmissionRunInfo | None:
    return (db.query(SubmissionRunInfo)
            .filter(SubmissionRunInfo.submission_run_info_id == id)
            .first())


def read_all(db: Session) -> [SubmissionRunInfo]:
    return db.query(SubmissionRunInfo).all()


def read_all_W_filter(db: Session, **kwargs) -> [SubmissionRunInfo]:
    return (db.query(SubmissionRunInfo)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, submission_run_info: SubmissionRunInfoBase) -> SubmissionRunInfo | None:
    db_submission_run_info: SubmissionRunInfo | None = (db.query(SubmissionRunInfo)
                                                        .filter(SubmissionRunInfo.submission_run_info_id == id)
                                                        .one_or_none())
    if db_submission_run_info is None:
        return

    for key, value in submission_run_info.model_dump().items():
        setattr(db_submission_run_info, key, value) if value is not None else None

    db.commit()
    db.refresh(db_submission_run_info)
    return db_submission_run_info


def delete(db: Session, id: int, submission_run_info: SubmissionRunInfoBase) -> None:
    db_submission_run_info: SubmissionRunInfo | None = (db.query(SubmissionRunInfo)
                                                        .filter(SubmissionRunInfo.submission_run_info_id == id)
                                                        .one_or_none())
    if db_submission_run_info is None:
        return

    db.delete(db_submission_run_info)
    db.commit()
