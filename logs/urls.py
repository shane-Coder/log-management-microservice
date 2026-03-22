from django.urls import path
from .views import (
    LogCreateView, 
    LogListView, 
    LogSearchView
)

urlpatterns = [
    path("logs", LogCreateView.as_view()),
    path("logs/list", LogListView.as_view()),
    path("logs/search", LogSearchView.as_view()),
]