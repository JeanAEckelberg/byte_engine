from sqlalchemy.orm import Session

from server.models.turn import Turn
from server.schemas.turn.turn_schema import TurnBase


def create(db: Session, turn: TurnBase) -> Turn:
    db_turn: Turn = Turn(**turn.model_dump(exclude={'turn_id'}))
    db.add(db_turn)
    db.commit()
    db.refresh(db_turn)
    return db_turn


def create_all(db: Session, turns: [TurnBase]) -> None:
    inserts: list[Turn] = [Turn(**turn.model_dump(exclude={'turn_id'})) for turn in turns]
    db.add_all(inserts)
    db.commit()


def read(db: Session, id: int) -> Turn | None:
    return (db.query(Turn)
            .filter(Turn.turn_id == id)
            .first())


def read_all(db: Session) -> [Turn]:
    return db.query(Turn).all()


def read_all_W_filter(db: Session, **kwargs) -> [Turn]:
    return (db.query(Turn)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, turn: TurnBase) -> Turn | None:
    db_turn: Turn | None = (db.query(Turn)
                            .filter(Turn.turn_id == id)
                            .one_or_none())
    if db_turn is None:
        return

    for key, value in turn.model_dump().items():
        setattr(db_turn, key, value) if value is not None else None

    db.commit()
    db.refresh(db_turn)
    return db_turn


def delete(db: Session, id: int, turn_table: TurnBase) -> None:
    db_turn: Turn | None = (db.query(Turn)
                            .filter(Turn.turn_id == id)
                            .one_or_none())
    if db_turn is None:
        return

    db.delete(db_turn)
    db.commit()
