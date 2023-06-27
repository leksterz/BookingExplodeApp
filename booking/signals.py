from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Booking
from django.db.models import Q


@receiver(post_save, sender=Booking)
def handle_booking_status_update(sender, instance, **kwargs):
    if instance.status == 'accepted':
        to_be_accepted_booking = instance
        pending_bookings = Booking.objects.filter(date=to_be_accepted_booking.date, status='pending')

        for booking in pending_bookings:
            if (
                (booking.start_time < to_be_accepted_booking.start_time and booking.end_time > to_be_accepted_booking.start_time) or
                (booking.start_time >= to_be_accepted_booking.start_time and booking.start_time < to_be_accepted_booking.end_time)
            ):
                booking.status = 'declined'
                booking.save()
