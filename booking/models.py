from django.db import models
from datetime import date

class Studio(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name} ({self.location})'


class Engineer(models.Model):
    name = models.CharField(max_length=255)
    start_work = models.TimeField()
    end_work = models.TimeField()
    contact_info = models.EmailField(null=True, blank=True)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    artist_name = models.CharField(max_length=255, default='John Doe')
    artist_phone_number = models.CharField(max_length=15, default='1234567890')
    artist_email = models.EmailField(default='john@example.com')
    date = models.DateField(default=date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Booking for {self.artist_name} with {self.engineer.name} at {self.studio.name} ({self.date}, {self.start_time} to {self.end_time})'

class Schedule(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
    ]

    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES, default='available')

    def __str__(self):
        return f'Schedule for {self.engineer.name} at {self.studio.name} ({self.start_time} to {self.end_time} on {self.date})'
