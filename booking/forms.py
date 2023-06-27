from datetime import timedelta, datetime
from django import forms
from .models import Booking, Schedule
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['artist_name', 'artist_phone_number', 'artist_email', 'engineer', 'studio', 'date', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist_name'].initial = ''
        self.fields['artist_phone_number'].initial = ''
        self.fields['artist_email'].initial = ''

    def clean_artist_phone_number(self):
        artist_phone_number = self.cleaned_data.get('artist_phone_number')

        # Check if the phone number matches the US phone number pattern
        if not re.match(r'^\+?1?[2-9]\d{2}[2-9]\d{2}\d{4}$', artist_phone_number):
            raise ValidationError("Invalid US phone number.")

        return artist_phone_number

    

    ## The clean method is called during form validation, after the individual field validations have passed. 
    # It is responsible for performing additional validation and cleaning the form data as needed.
    # In the clean method, we retrieve the values of the relevant fields 
    # (start_time, end_time, date, studio) from the form's cleaned_data dictionary.
    # We first check if the start_time and end_time are equal. If they are, we raise a validation 
    # error because a booking with zero duration is not valid.
    # Next, we query the Schedule model to check if there are any available time slots that overlap with the selected start_time 
    # and end_time. The Schedule objects should have the same studio, date, and fall within the range of the selected start_time and end_time.
    # If any available time slots are found (schedule_qs is not empty), 
    # it means that the selected start_time and end_time are within the available schedule, and the booking is considered valid.
    # If no available time slots are found (schedule_qs is empty), 
    # we raise a validation error indicating that the selected start_time and end_time are invalid.

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        date = cleaned_data.get('date')
        studio = cleaned_data.get('studio')
        engineer = cleaned_data.get('engineer')

        errors = {}

        if start_time and end_time and date and studio and engineer:
            if start_time == end_time:
                errors['start_time'] = "Start time and end time cannot be the same."
            
            # Check if the selected time duration is not an exact 1 hr time increment
            start_datetime = datetime.combine(datetime.today(), start_time)
            end_datetime = datetime.combine(datetime.today(), end_time)
            selected_duration = end_datetime - start_datetime

            if selected_duration.total_seconds() % 3600 != 0:
                errors['start_time'] = "Selected duration must be in full-hour increments."

            # Check if the selected start time is available in the schedule 
            start_time_exists = Schedule.objects.filter(
                studio=studio,
                date=date,
                start_time=start_time,
                availability='available'
            ).exists()

            if not start_time_exists:
                errors['start_time'] = "Invalid start time. Please select an available start time."

            # Check if the selected date maps to any Schedule objects
            if not Schedule.objects.filter(date=date).exists():
                errors['date'] = "No schedule available for the selected date."

            schedule_qs = Schedule.objects.filter(
                studio=studio,
                date=date,
                start_time__lte=end_time,
                end_time__gte=start_time,
                availability='available'
            ).order_by('start_time')

            if not schedule_qs.exists():
                errors['studio'] = "Invalid studio selection. The studio is unavailable for the selected time, date, or engineer."

            available_slots = []
            current_slot_start = start_time

            for slot in schedule_qs:
                if slot.start_time >= current_slot_start:
                    available_slots.append(slot)
                    current_slot_start = slot.end_time

                if current_slot_start > end_time:
                    break

            total_duration = timedelta()
            for slot in available_slots:
                total_duration += timedelta(hours=slot.end_time.hour - slot.start_time.hour)

            if total_duration < selected_duration:
                errors['start_time'] = "Invalid start time or end time."

        if errors:
            raise ValidationError(errors)

        return cleaned_data


