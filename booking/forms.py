from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['artist_name', 'artist_phone_number', 'artist_email', 'engineer', 'studio', 'date', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist_name'].initial = ''
        self.fields['artist_phone_number'].initial = ''
        self.fields['artist_email'].initial = ''
