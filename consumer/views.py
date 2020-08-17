from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from business.models import Company
from .models import Bookings
# Create your views here.

@login_required
def bookingScheduleView(request, id, slug):
    company = get_object_or_404(Company, id=id, slug=slug, available=True)
    bookings = Bookings.objects.filter(company=company)
    return render(request, 'business/booking/bookingCalendar.html', {'company':company, 'bookings':bookings})

@login_required
def FutPastBooking(request):
    my_companies = Company.objects.filter(user=request.user)
    return render(request, 'account/bookingsched.html',{'my_companies':my_companies})

