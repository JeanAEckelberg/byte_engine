from sqlalchemy.orm import Session

from server.models.tournament import Tournament
from server.schemas.tournament.tournament_base import TournamentBase
from server.schemas.tournament.tournament_schema import TournamentSchema


def create(db: Session, tournament: TournamentBase) -> Tournament:
    db_tournament: Tournament = Tournament(**tournament.model_dump(exclude={'tournament_id'}))
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def read(db: Session, id: int) -> Tournament | None:
    return (db.query(Tournament)
            .filter(Tournament.tournament_id == id)
            .first())


def read_all(db: Session) -> [Tournament]:
    return db.query(Tournament).all()


def read_all_W_filter(db: Session, **kwargs) -> [Tournament]:
    return (db.query(Tournament)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, tournament: TournamentBase) -> Tournament | None:
    db_tournament: Tournament | None = (db.query(Tournament)
                                     .filter(Tournament.tournament_id == id)
                                     .one_or_none())
    if db_tournament is None:
        return

    for key, value in tournament.model_dump().items():
        setattr(db_tournament, key, value) if value is not None else None

    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def delete(db: Session, id: int) -> None:
    db_tournament: Tournament | None = (db.query(Tournament)
                                     .filter(Tournament.tournament_id == id)
                                     .one_or_none())
    if db_tournament is None:
        return

    db.delete(db_tournament)
    db.commit()
