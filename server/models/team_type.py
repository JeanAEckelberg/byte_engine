from server.models.base import Base
from sqlalchemy import LargeBinary, Boolean, Column, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column


class TeamType(Base):
    __tablename__ = 'team_type'
    team_type_id: Mapped[int] = mapped_column(primary_key=True)
    team_type_name: Mapped[str] = mapped_column(String(15), nullable=False,
                                                constraint=CheckConstraint("team_type_name != ''"))
    eligible: bool = mapped_column(Boolean(), nullable=False)
