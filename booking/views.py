from django.shortcuts import render, redirect
from .models import Schedule
from .forms import BookingForm
from django.views.generic import TemplateView


def BookingView(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking:confirmation')  # Redirect to the confirmation page
    else:
        form = BookingForm()
    
    schedule_list = Schedule.objects.all()  # Fetch all schedule entries

    context = {
        'form': form,
        'schedule_list': schedule_list,
    }
    return render(request, 'booking/booking.html', context)


def schedule_view(request):
    # Fetch schedule data from the database
    schedule_data = Schedule.objects.all()

    # Pass the schedule data to the template
    context = {'schedule_data': schedule_data}

    # Render the template and return the response
    return render(request, 'booking/schedule.html', context)

# Create your views here.

class ConfirmationView(TemplateView):
    template_name = 'booking/confirmation.html'