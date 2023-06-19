from django.shortcuts import render

from .models import Schedule

def schedule_view(request):
    # Fetch schedule data from the database
    schedule_data = Schedule.objects.all()

    # Pass the schedule data to the template
    context = {'schedule_data': schedule_data}

    # Render the template and return the response
    return render(request, 'booking/schedule.html', context)

# Create your views here.
