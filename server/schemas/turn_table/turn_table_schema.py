from server.schemas.run.run_base import RunBase
from server.schemas.turn_table.turn_table_base import TurnTableBase


class TurnTableSchema(TurnTableBase):
    run: RunBase
