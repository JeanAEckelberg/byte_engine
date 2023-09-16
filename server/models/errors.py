from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class Errors(Base):
    __tablename__: str = 'errors'
    run_id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # run id pk
    run_id_fk: Mapped[int] = mapped_column(Integer(), ForeignKey("run.run_id"))  # run id
    submission_id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # submission id
    submission_id_fk: Mapped[int] = mapped_column(Integer(), ForeignKey("submission.submission_id"))  # submission id fk
    error_txt: Mapped[str] = mapped_column(String(), nullable=True)



