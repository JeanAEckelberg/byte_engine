from sqlalchemy.orm import Session

from server.models.team_type import TeamType
from server.schemas.team_type.team_type_schema import TeamTypeBase


def create(db: Session, team_type: TeamTypeBase) -> TeamType:
    db_team_type: TeamType = TeamType(**team_type.model_dump(exclude={'team_type_id'}))
    db.add(db_team_type)
    db.commit()
    db.refresh(db_team_type)
    return db_team_type


def read(db: Session, id: int) -> TeamType | None:
    return (db.query(TeamType)
            .filter(TeamType.team_type_id == id)
            .first())


def read_all(db: Session) -> [TeamType]:
    return db.query(TeamType).all()


def read_all_W_filter(db: Session, **kwargs) -> [TeamType]:
    return (db.query(TeamType)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, team_type: TeamTypeBase) -> TeamType | None:
    db_team_type: TeamType | None = (db.query(TeamType)
                                     .filter(TeamType.team_type_id == id)
                                     .one_or_none())
    if db_team_type is None:
        return

    for key, value in team_type.model_dump().items():
        setattr(db_team_type, key, value) if value is not None else None

    db.commit()
    db.refresh(db_team_type)
    return db_team_type


def delete(db: Session, id: int, team_type: TeamTypeBase) -> None:
    db_team_type: TeamType | None = (db.query(TeamType)
                                     .filter(TeamType.team_type_id == id)
                                     .one_or_none())
    if db_team_type is None:
        return

    db.delete(db_team_type)
    db.commit()
