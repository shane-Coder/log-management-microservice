from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import LogEntry
from .serializers import LogEntrySerializer

from event_stream.producer import send_logs
from .alerting import check_error_threshold

class LogCreateView(APIView):
    def post(self, request):
        logs = request.data
        if not isinstance(logs, list):
            logs = [logs]
        serializer = LogEntrySerializer(data=logs, many=True)
        serializer.is_valid(raise_exception=True)
        send_logs(serializer.validated_data)
        return Response(
            {"message": f"{len(logs)} logs pushed to Kafka"},
            status=status.HTTP_202_ACCEPTED
        )
    
class LogListView(APIView):
    def get(self, request):
        logs = LogEntry.objects.order_by("-timestamp")[:50]
        result = []
        for log in logs:
            result.append({
                "service_name": log.service_name,
                "level": log.level,
                "message": log.message,
                "timestamp": log.timestamp,
                "metadata": log.metadata
            })
        return Response(result)

class LogSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q")
        if query:
            logs = LogEntry.objects.filter(
                __raw__={
                    "$or": [
                        {"message": {"$regex": query, "$options": "i"}},
                        {"service_name": {"$regex": query, "$options": "i"}}
                    ]
                }
            ).order_by("-timestamp")[:100]
        else:
            logs = LogEntry.objects.order_by("-timestamp")[:100]
        result = []
        for log in logs:
            result.append({
                "service_name": log.service_name,
                "level": log.level,
                "message": log.message,
                "timestamp": log.timestamp,
                "metadata": log.metadata
            })
        return Response(result)
    
class ErrorsPerServiceView(APIView):
    def get(self, request):
        pipeline = [
            {"$match": {"level": "ERROR"}},
            {"$group": {
                "_id": "$service_name",
                "error_count": {"$sum": 1}
            }},
            {"$sort": {"error_count": -1}}
        ]

        result = list(LogEntry.objects.aggregate(pipeline))

        return Response([
            {"service_name": i["_id"], "error_count": i["error_count"]}
            for i in result
        ])

class LogsPerServiceView(APIView):
    def get(self, request):
        pipeline = [
            {"$group": {
                "_id": "$service_name",
                "log_count": {"$sum": 1}
            }},
            {"$sort": {"log_count": -1}}
        ]

        result = list(LogEntry.objects.aggregate(pipeline))

        return Response([
            {"service_name": i["_id"], "log_count": i["log_count"]}
            for i in result
        ])
    
class LogLevelDistributionView(APIView):
    def get(self, request):
        pipeline = [
            {"$group": {
                "_id": "$level",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]

        result = list(LogEntry.objects.aggregate(pipeline))

        return Response([
            {"level": i["_id"], "count": i["count"]}
            for i in result
        ])
    
class LogsPerMinuteView(APIView):
    def get(self, request):
        pipeline = [
            {"$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d %H:%M",
                        "date": "$timestamp"
                    }
                },
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]

        result = list(LogEntry.objects.aggregate(pipeline))
        return Response(result)
    
class ErrorsPerHourView(APIView):
    def get(self, request):
        pipeline = [
            {"$match": {"level": "ERROR"}},
            {"$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d %H",
                        "date": "$timestamp"
                    }
                },
                "count": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]

        result = list(LogEntry.objects.aggregate(pipeline))
        return Response(result)
    
class AlertView(APIView):
    def get(self, request):
        alerts = check_error_threshold()
        return Response({
            "alerts": alerts
        })