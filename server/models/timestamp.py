from datetime import datetime, timezone
import sqlalchemy as sa


class TimeStamp(sa.types.TypeDecorator):
    impl = sa.types.DateTime
    LOCAL_TIMEZONE = datetime.utcnow().astimezone().tzinfo

# if datetime is none, returns datetime. if timezone is none, returns local timezone.
    def process_bind_param(self, value: datetime, dialect):
        if value is None:
            return datetime.utcnow()
        if value.tzinfo is None:
            value = value.astimezone(self.LOCAL_TIMEZONE)

        return value.astimezone(timezone.utc)

# changes timezone to utc timezone
    def process_result_value(self, value: datetime, dialect):
        if value is None:
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
