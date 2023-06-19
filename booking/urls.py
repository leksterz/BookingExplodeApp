from django.urls import path
from .views import schedule_view

app_name = 'app'

urlpatterns = [
    path('schedule/', schedule_view, name='schedule'),
    # Other app-specific URLs
]
