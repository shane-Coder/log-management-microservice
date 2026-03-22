import mongoengine as me
from datetime import datetime, timezone

class LogEntry(me.Document):
    service_name = me.StringField(required=True)
    level = me.StringField(
        required=True,
        choices=["INFO", "ERROR", "WARNING", "DEBUG"]
    )
    message = me.StringField(required=True)
    timestamp = me.DateTimeField(required=True)
    metadata = me.DictField()
    created_at = me.DateTimeField(default=lambda: datetime.now(timezone.utc))
    meta = {
        "collection": "logs",
        "indexes": [
            "service_name",
            "level",
            "timestamp",
            # compound indexes (VERY IMPORTANT)
            ("service_name", "timestamp"),
            ("level", "timestamp"),
        ]
    }