from sqlalchemy.orm import Session
from sqlalchemy import and_

from server.models.run import Run
from server.schemas.run_schema import RunBase, RunSchema


def create(db: Session, run: RunBase) -> Run:
    db_run: Run = Run(**run.model_dump(exclude={'run_id'}))
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


def read(db: Session, id: int) -> Run | None:
    return (db.query(Run)
            .filter(Run.run_id == id)
            .first())


def read_all(db: Session) -> [Run]:
    return db.query(Run).all()


def read_all_W_filter(db: Session, **kwargs) -> [Run]:
    return (db.query(Run)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, run: RunBase) -> Run | None:
    db_run: Run | None = (db.query(Run)
                                .filter(Run.run_id == id)
                                .one_or_none())
    if db_run is None:
        return

    for key, value in run.model_dump().items():
        setattr(db_run, key, value) if value is not None else None

    db.commit()
    db.refresh(db_run)
    return db_run


def delete(db: Session, id: int, run: RunBase) -> None:
    db_run: Run | None = (db.query(Run)
                                .filter(Run.run_id == id)
                                .one_or_none())
    if db_run is None:
        return

    db.delete(db_run)
    db.commit()
