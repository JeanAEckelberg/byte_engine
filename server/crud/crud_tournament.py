from sqlalchemy.orm import Session, joinedload

from server.models.run import Run
from server.models.submission import Submission
from server.models.submission_run_info import SubmissionRunInfo
from server.models.team import Team
from server.models.tournament import Tournament
from server.schemas.tournament.tournament_base import TournamentBase
from server.schemas.tournament.tournament_schema import TournamentSchema


def create(db: Session, tournament: TournamentBase) -> Tournament:
    db_tournament: Tournament = Tournament(**tournament.model_dump(exclude={'tournament_id'}))
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def read(db: Session, id: int, eager: bool = False) -> Tournament | None:
    return (db.query(Tournament)
            .filter(Tournament.tournament_id == id)
            .first() if not eager
            else db.query(Tournament)
            .options(joinedload(Tournament.runs)
                     .joinedload(Run.submission_run_infos)
                     .joinedload(SubmissionRunInfo.submission)
                     .joinedload(Submission.team),
                     joinedload(Tournament.runs)
                     .joinedload(Run.turns))
            .filter(Tournament.tournament_id == id)
            .first())


def read_all(db: Session, eager: bool = False) -> [Tournament]:
    return (db.query(Tournament)
            .all() if not eager
            else db.query(Tournament)
            .options(joinedload(Tournament.runs)
                     .joinedload(Run.submission_run_infos)
                     .joinedload(SubmissionRunInfo.submission)
                     .joinedload(Submission.team),
                     joinedload(Tournament.runs)
                     .joinedload(Run.turns))
            .all())


def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [Tournament]:
    return (db.query(Tournament)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(Tournament)
            .options(joinedload(Tournament.runs)
                     .joinedload(Run.submission_run_infos)
                     .joinedload(SubmissionRunInfo.submission)
                     .joinedload(Submission.team),
                     joinedload(Tournament.runs)
                     .joinedload(Run.turns))
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
