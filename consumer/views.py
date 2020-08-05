from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from business.models import Company
# Create your views here.

@login_required
def bookingScheduleView(request, id, slug):
    company = get_object_or_404(Company, id=id, slug=slug, available=True)
    return render(request, 'business/booking/bookingCalendar.html', {'company':company})