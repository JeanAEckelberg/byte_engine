from sqlalchemy.orm import Session
from sqlalchemy import and_

from server.models.turn_table import TurnTable
from server.schemas.turn_table_schema import TurnTableBase, TurnTableSchema


def create(db: Session, turn_table: TurnTableBase) -> TurnTable:
    db_turn_table: TurnTable = TurnTable(**turn_table.model_dump(exclude={'turn_id'}))
    db.add(db_turn_table)
    db.commit()
    db.refresh(db_turn_table)
    return db_turn_table

def create_all(db: Session, turn_tables: [TurnTableBase]) -> None:
    inserts: list[TurnTable] = [TurnTable(**turn_table.model_dump(exclude={'turn_id'})) for turn_table in turn_tables]
    db.add_all(inserts)
    db.commit()


def read(db: Session, id: int) -> TurnTable | None:
    return (db.query(TurnTable)
            .filter(TurnTable.turn_id == id)
            .first())


def read_all(db: Session) -> [TurnTable]:
    return db.query(TurnTable).all()


def read_all_W_filter(db: Session, **kwargs) -> [TurnTable]:
    return (db.query(TurnTable)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, turn_table: TurnTableBase) -> TurnTable | None:
    db_turn_table: TurnTable | None = (db.query(TurnTable)
                                       .filter(TurnTable.turn_id == id)
                                       .one_or_none())
    if db_turn_table is None:
        return

    for key, value in turn_table.model_dump().items():
        setattr(db_turn_table, key, value) if value is not None else None

    db.commit()
    db.refresh(db_turn_table)
    return db_turn_table


def delete(db: Session, id: int, turn_table: TurnTableBase) -> None:
    db_turn_table: TurnTable | None = (db.query(TurnTable)
                                       .filter(TurnTable.turn_id == id)
                                       .one_or_none())
    if db_turn_table is None:
        return

    db.delete(db_turn_table)
    db.commit()
