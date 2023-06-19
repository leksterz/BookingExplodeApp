from django import forms
from .models import Booking, Schedule
from django.core.exceptions import ValidationError
from django.utils import timezone



class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['artist_name', 'artist_phone_number', 'artist_email', 'engineer', 'studio', 'date', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist_name'].initial = ''
        self.fields['artist_phone_number'].initial = ''
        self.fields['artist_email'].initial = ''

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        date = cleaned_data.get('date')
        studio = cleaned_data.get('studio')

        if start_time and end_time and date and studio:
            # Check if the selected start time and end time are within the available schedule
            schedule_qs = Schedule.objects.filter(
                studio=studio,
                date=date,
                start_time__lte=start_time,
                end_time__gte=end_time
            )
            if not schedule_qs.exists():
                raise ValidationError("Invalid start time or end time.")

            # Check if there are any conflicting bookings for the selected start time and end time
            # booking_qs = Booking.objects.filter(
            #     studio=studio,
            #     date=date,
            #     start_time__lte=start_time,
            #     end_time__gte=end_time
            # )
            # if booking_qs.exists():
            #     raise ValidationError("The selected time slot is already booked.")
        return cleaned_data

