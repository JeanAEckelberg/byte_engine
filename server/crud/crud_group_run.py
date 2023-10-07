
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


def update(db: Session, id: int, group_run: GroupRunBase) -> GroupRun | None:
    db_group_run: GroupRun | None = (db.query(GroupRun)
                                        .filter(and_(GroupRun.group_run_id == id,
                                                     GroupRun.is_finished == group_run.is_finished))
                                        .one_or_none())
    if db_group_run is None:
        return

    for group_run.is_finished, group_run_id in group_run.model_dump().items():
        setattr(db_group_run, group_run.is_finished, True) if group_run_id == group_run_id else False

    db.commit()
    db.refresh(db_group_run)
    return db_group_run


def delete(db: Session, id: int, submission: GroupRunBase) -> None:
    db_group_run: GroupRun | None = (db.query(GroupRun)
                                        .filter(GroupRun.group_run_id == id)
                                        .one_or_none())
    if db_group_run is None:
        return

    db.delete(db_group_run)
    db.commit()
