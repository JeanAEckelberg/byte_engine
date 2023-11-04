from sqlalchemy.orm import Session

from server.models.team import Team
from server.schemas.team.team_schema import TeamBase


def create(team: TeamBase, db: Session) -> Team:
    db_team: Team = Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def read(db: Session, id: int) -> Team | None:
    return (db.query(Team)
            .filter(Team.team_uuid == id)
            .first())


def read_all(db: Session) -> [Team]:
    return db.query(Team).all()


def read_all_W_filter(db: Session, **kwargs) -> [Team]:
    return (db.query(Team)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, team: TeamBase) -> Team | None:
    db_team: Team | None = (db.query(Team)
                            .filter(Team.team_uuid == id)
                            .one_or_none())
    if db_team is None:
        return

    for key, value in team.model_dump().items():
        setattr(db_team, key, value) if value is not None else None

    db.commit()
    db.refresh(db_team)
    return db_team


def delete(db: Session, id: int, team: TeamBase) -> None:
    db_team: Team | None = (db.query(Team)
                                        .filter(Team.team_uuid == id)
                                        .one_or_none())
    if db_team is None:
        return

    db.delete(db_team)
    db.commit()
