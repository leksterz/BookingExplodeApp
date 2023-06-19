from django.urls import path
from .views import schedule_view,  BookingView, ConfirmationView

app_name = 'app'

urlpatterns = [
    path('schedule/', schedule_view, name='schedule'),
    path('book/', BookingView, name='book'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),

    
]
