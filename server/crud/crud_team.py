from sqlalchemy.orm import Session, joinedload

from server.models.team import Team
from server.schemas.team.team_schema import TeamBase


# create method for team
def create(team: TeamBase, db: Session) -> Team:
    db_team: Team = Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


# read most recent team
def read(db: Session, id: int, eager: bool = False) -> Team | None:
    return (db.query(Team)
            .filter(Team.team_uuid == id)
            .first() if not eager
            else db.query(Team)
            .options(joinedload(Team.university),
                     joinedload(Team.team_type),
                     joinedload(Team.submissions))
            .filter(Team.team_uuid == id)
            .first())


# read all teams
def read_all(db: Session, eager: bool = False) -> [Team]:
    return (db.query(Team)
            .all() if not eager
            else db.query(Team)
            .options(joinedload(Team.university),
                     joinedload(Team.team_type),
                     joinedload(Team.submissions))
            .all())


# read a specified team
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [Team]:
    return (db.query(Team)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(Team)
            .options(joinedload(Team.university),
                     joinedload(Team.team_type),
                     joinedload(Team.submissions))
            .all())


# update a team
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


# delete a team
def delete(db: Session, id: int, team: TeamBase) -> None:
    db_team: Team | None = (db.query(Team)
                                        .filter(Team.team_uuid == id)
                                        .one_or_none())
    if db_team is None:
        return

    db.delete(db_team)
    db.commit()
