from server.schemas.tournament.tournament_base import TournamentBase
from server.schemas.run.run_schema_wo_tournament import RunSchemaWithoutTournament


class TournamentSchema(TournamentBase):
    runs: list[RunSchemaWithoutTournament]
