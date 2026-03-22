from datetime import datetime, timedelta, timezone
from logs.models import LogEntry

def check_error_threshold():
    last_5_min = datetime.now(timezone.utc) - timedelta(minutes=5)
    print("NOW:", datetime.now(timezone.utc))
    print("LAST_5_MIN:", last_5_min)
    pipeline = [
        {
            "$match": {
                "level": "ERROR",
                "timestamp": {"$gte": last_5_min}
            }
        },
        {
            "$group": {
                "_id": "$service_name",
                "error_count": {"$sum": 1}
            }
        }
    ]

    results = list(LogEntry.objects.aggregate(pipeline))
    print(results)

    alerts = []

    for item in results:
        if item["error_count"] > 2:
            alerts.append({
                "service": item["_id"],
                "error_count": item["error_count"]
            })
            print(f"🚨 ALERT: {item['_id']} has {item['error_count']} errors in last 5 min")

    return alerts