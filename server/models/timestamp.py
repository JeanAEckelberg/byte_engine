from datetime import datetime, timezone
import sqlalchemy as sa


class TimeStamp(sa.types.TypeDecorator):
    impl = sa.types.DateTime

    def process_bind_param(self, value: datetime, dialect):
        if value is None:
            return datetime.utcnow()

        return value

    def process_result_value(self, value: datetime, dialect):
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value
