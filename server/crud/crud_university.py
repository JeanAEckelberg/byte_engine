from sqlalchemy.orm import Session

from server.models.university import University
from server.schemas.university.university_schema import UniversityBase


def create(db: Session, university: UniversityBase) -> University:
    db_university: University = University(**university.model_dump(exclude={'uni_id'}))
    db.add(db_university)
    db.commit()
    db.refresh(db_university)
    return db_university


def read(db: Session, id: int) -> University | None:
    return (db.query(University)
            .filter(University.uni_id == id)
            .first())


def read_all(db: Session) -> [University]:
    return db.query(University).all()


def read_all_W_filter(db: Session, **kwargs) -> [University]:
    return (db.query(University)
            .filter_by(**kwargs)
            .all())


def update(db: Session, id: int, university: UniversityBase) -> University | None:
    db_university: University | None = (db.query(University)
                                        .filter(University.uni_id == id)
                                        .one_or_none())
    if db_university is None:
        return

    for key, value in university.model_dump().items():
        setattr(db_university, key, value) if value is not None else None

    db.commit()
    db.refresh(db_university)
    return db_university


def delete(db: Session, id: int, university: UniversityBase) -> None:
    db_university: University | None = (db.query(University)
                                        .filter(University.uni_id == id)
                                        .one_or_none())
    if db_university is None:
        return

    db.delete(db_university)
    db.commit()
