from server.schemas.team.team_base import TeamBase
from server.schemas.university.university_base import UniversityBase


# University <-> Team: Many to One
# Schema for University using UniversityBase and includes its relations
class UniversitySchema(UniversityBase):
    teams: list[TeamBase]
