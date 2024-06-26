from sqlalchemy import LargeBinary, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Turn(Base):
    """
    'Turn' Model Class
    turn_id: primary key
    turn_number
    run_id: foreign key
    turn_data

    Related table:
        * run
    """

    __tablename__: str = 'turn'
    turn_number: Mapped[int] = mapped_column(Integer(), nullable=False, primary_key=True)
    run_id: Mapped[int] = mapped_column(Integer(), ForeignKey('run.run_id', ondelete='CASCADE'), primary_key=True)
    turn_data: Mapped[str] = mapped_column(LargeBinary(), nullable=False)

    run: Mapped['Run'] = relationship(back_populates='turns', passive_deletes=True)
