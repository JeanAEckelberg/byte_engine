from server.models.base import Base
from sqlalchemy import LargeBinary, Boolean, Column, CheckConstraint, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import uuid4

class Submission(Base):
    __tablename__: str = 'submission'
    submission_id: Mapped[int] = mapped_column(Integer(), primary_key=True, default=uuid4())
    team_id_uuid: Mapped[int] = mapped_column(Integer(), ForeignKey("team.team_id_uuid"))
    submission_time: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    file_txt: Mapped[str] = mapped_column(LargeBinary(), nullable=False)
