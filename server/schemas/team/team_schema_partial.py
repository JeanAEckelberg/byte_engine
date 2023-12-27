from server.schemas.submission.submission_partial import SubmissionSchemaPartial
from server.schemas.team.team_base import TeamBase
from server.schemas.team_type.team_type_schema import TeamTypeBase
from server.schemas.university.university_schema import UniversityBase


# University <-> Team: Many to One
# Schema for Team using TeamBase and includes its relations ~ submission relation is partial submission
class TeamSchemaPartial(TeamBase):
    university: UniversityBase
    team_type: TeamTypeBase
    submissions: list[SubmissionSchemaPartial]
