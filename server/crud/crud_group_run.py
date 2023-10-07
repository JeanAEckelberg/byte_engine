from sqlalchemy.orm import Session
from sqlalchemy import and_

from server.models.group_run import GroupRun
from server.schemas.group_run_schema import GroupRunSchema, GroupRunBase


def create(db: Session, group_run: GroupRunBase) -> GroupRun:
    db_group_run: GroupRun = GroupRun(**group_run.model_dump(exclude={'group_run_id'}))
    db.add(db_group_run)
    db.commit()
    db.refresh(db_group_run)
    return db_group_run


def read(db: Session, id: int) -> GroupRun | None:
    return (db.query(GroupRun)
            .filter(GroupRun.group_run_id == id)
            .first())


def read_all(db: Session) -> [GroupRun]:
    return db.query(GroupRun).all()


def read_all_W_filter(db: Session, **kwargs) -> [GroupRun]:
    return (db.query(GroupRun)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, group_run: GroupRunBase) -> GroupRun | None:
    db_group_run: GroupRun | None = (db.query(GroupRun)
                                     .filter(GroupRun.group_run_id == id)
                                     .one_or_none())
    if db_group_run is None:
        return

    for key, value in group_run.model_dump().items():
        setattr(db_group_run, key, value) if value is not None else None

    db.commit()
    db.refresh(db_group_run)
    return db_group_run


def delete(db: Session, id: int, group_run: GroupRunBase) -> None:
    db_group_run: GroupRun | None = (db.query(GroupRun)
                                     .filter(GroupRun.group_run_id == id)
                                     .one_or_none())
    if db_group_run is None:
        return

    db.delete(db_group_run)
    db.commit()
