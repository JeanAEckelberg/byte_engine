import uuid
from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import and_

from server.models.errors import Errors
from server.schemas.errors_schema import ErrorsBase, ErrorsSchema


def create(db: Session, errors: ErrorsBase) -> Errors:
    db_errors: Errors = Errors(**errors.model_dump(exclude={'errors_id'}))
    db.add(db_errors)
    db.commit()
    db.refresh(db_errors)
    return db_errors


def read(db: Session, id: int) -> Errors | None:
    return (db.query(Errors)
            .filter(Errors.error_id == id)
            .first())


def read_all(db: Session) -> [Errors]:
    return db.query(Errors).all()


def read_all_W_filter(db: Session, **kwargs) -> [Errors]:
    return (db.query(Errors)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, errors: ErrorsBase) -> Errors | None:
    db_errors: Errors | None = (db.query(Errors)
                                .filter(Errors.error_id == id)
                                .one_or_none())
    if db_errors is None:
        return

    for key, value in errors.model_dump().items():
        setattr(db_errors, key, value) if value is not None else None

    db.commit()
    db.refresh(db_errors)
    return db_errors


def delete(db: Session, id: int, errors: ErrorsBase) -> None:
    db_errors: Errors | None = (db.query(Errors)
                                .filter(Errors.error_id == id)
                                .one_or_none())
    if db_errors is None:
        return

    db.delete(db_errors)
    db.commit()
