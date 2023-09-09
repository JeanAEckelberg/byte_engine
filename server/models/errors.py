from server.models.base import Base
from sqlalchemy import LargeBinary, Boolean, Column, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Errors(Base):
    __tablename__: str = 'errors'
    run_id: Mapped[int] = mapped_column(Integer(), ForeignKey("run.run_id"), primary_key=True)
    submission_id: Mapped[int] = mapped_column(Integer(), ForeignKey("submission.submission_id"), primary_key=True)
    error_txt: Mapped[String] = mapped_column(String(), nullable=True)



