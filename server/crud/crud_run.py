from sqlalchemy.orm import Session, joinedload

from server.models.run import Run
from server.schemas.run.run_schema import RunBase


# Create method for Run
def create(db: Session, run: RunBase) -> Run:
    db_run: Run = Run(**run.model_dump(exclude={'run_id'}))
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run


# read the most recent run
def read(db: Session, id: int, eager: bool = False) -> Run | None:
    return (db.query(Run)
            .filter(Run.run_id == id)
            .first() if not eager
            else db.query(Run)
            .options(joinedload(Run.turns),
                     joinedload(Run.submission_run_infos),
                     joinedload(Run.tournament))
            .filter(Run.run_id == id)
            .first())


# read all runs
def read_all(db: Session, eager: bool = False) -> [Run]:
    return db.query(Run).all() if not eager \
        else db.query(Run).options(joinedload(Run.turns),
                                   joinedload(Run.submission_run_infos),
                                   joinedload(Run.tournament)).all()


# read a specified run
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [Run]:
    return (db.query(Run)
            .filter_by(**kwargs)
            .all() if not eager else
            db.query(Run)
            .options(joinedload(Run.turns),
                     joinedload(Run.submission_run_infos),
                     joinedload(Run.tournament))
            .filter_by(**kwargs).all())


# Update a run
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


# delete a run
def delete(db: Session, id: int, run: RunBase) -> None:
    db_run: Run | None = (db.query(Run)
                          .filter(Run.run_id == id)
                          .one_or_none())
    if db_run is None:
        return

    db.delete(db_run)
    db.commit()
