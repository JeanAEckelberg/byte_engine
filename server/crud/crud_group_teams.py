from sqlalchemy.orm import Session

from server.models.group_teams import GroupTeams
from server.schemas.group_teams.group_teams_schema import GroupTeamsBase


def create(db: Session, group_teams: GroupTeamsBase) -> GroupTeams:
    db_group_teams: GroupTeams = GroupTeams(**group_teams.model_dump(exclude={'group_teams_id'}))
    db.add(db_group_teams)
    db.commit()
    db.refresh(db_group_teams)
    return db_group_teams


def read(db: Session, id: int) -> GroupTeams | None:
    return (db.query(GroupTeams)
            .filter(GroupTeams.group_teams_id == id)
            .first())


def read_all(db: Session) -> [GroupTeams]:
    return db.query(GroupTeams).all()


def read_all_W_filter(db: Session, **kwargs) -> [GroupTeams]:
    return (db.query(GroupTeams)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, group_teams: GroupTeamsBase) -> GroupTeams | None:
    db_group_teams: GroupTeams | None = (db.query(GroupTeams)
                                         .filter(GroupTeams.group_teams_id == id)
                                         .one_or_none())
    if db_group_teams is None:
        return

    for key, value in group_teams.model_dump().items():
        setattr(db_group_teams, key, value) if value is not None else None

    db.commit()
    db.refresh(db_group_teams)
    return db_group_teams


def delete(db: Session, id: int, group_teams: GroupTeamsBase) -> None:
    db_group_teams: GroupTeams | None = (db.query(GroupTeams)
                                         .filter(GroupTeams.group_teams_id == id)
                                         .one_or_none())
    if db_group_teams is None:
        return

    db.delete(db_group_teams)
    db.commit()
