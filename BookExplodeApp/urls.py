from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include('booking.urls', namespace='booking')),
    # Other top-level URLs
]
