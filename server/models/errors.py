from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class Errors(Base):
    __tablename__: str = 'errors'
    run_id: Mapped[int] = mapped_column(Integer(), ForeignKey("run.run_id"), primary_key=True)
    submission_id: Mapped[int] = mapped_column(Integer(), ForeignKey("submission.submission_id"), primary_key=True)
    error_txt: Mapped[str] = mapped_column(String(), nullable=True)



