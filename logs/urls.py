from django.urls import path
from .views import *

urlpatterns = [
    path("logs", LogCreateView.as_view()),
    path("logs/list", LogListView.as_view()),
    path("logs/search", LogSearchView.as_view()),
    # Analytics
    path("analytics/errors-per-service", ErrorsPerServiceView.as_view()),
    path("analytics/logs-per-service", LogsPerServiceView.as_view()),
    path("analytics/log-level-distribution", LogLevelDistributionView.as_view()),
    path("analytics/logs-per-minute", LogsPerMinuteView.as_view()),
    path("analytics/errors-per-hour", ErrorsPerHourView.as_view()),
    # Alerts
    path("alerts", AlertView.as_view()),
]