from django.shortcuts import render, get_object_or_404
from business.models import Company, Services, OpeningHours
from consumer.models import Bookings
from django.http import JsonResponse
from django.views import View
import json
from django.core import serializers
import datetime
# Create your views here.


def get_companyslug(request, slug):
    request.viewing_company = get_object_or_404(Company, slug=slug)

def bookingurl(request):
    user = request.user
    company = request.viewing_company
    services = Services.objects.filter(business=company)
    return render(request, 'bookingpage/home.html', {'user': user, 'company':company, 'services':services})

def bookingServiceView(request, pk):
    user = request.user
    company = request.viewing_company
    service = get_object_or_404(Services, id=pk)
    return render(request, 'bookingpage/indservice.html', {'user': user, 'company':company, 'service':service})

def bizadmin(request):
    user = request.user
    return render(request, 'businessadmin/bizadmin.html', {'user': user})

def time_slots(start_time, end_time, interval):
    t = start_time
    print(t)
    while t <= end_time:
        yield t.strftime('%I:%M %p')
        t = (datetime.datetime.combine(datetime.date.today(), t) +
             datetime.timedelta(minutes=interval)).time()

class bookingTimes(View):
    def post(self, request):
        data=json.loads(request.body)
        s_id = data['id']
        month = data['month']
        year = data['year']
        day = data['day']
        weekday = data['weekday']
        company = request.viewing_company
        open_hours = get_object_or_404(OpeningHours,company=company, weekday=weekday)
        #We need to add the service time and validate whether the service can be fit in the timeslot
        b_open = open_hours.from_hour
        b_close = open_hours.to_hour
        interval= company.interval
        if open_hours.is_closed==False:
            slist = list(time_slots(b_open,b_close,interval))
        else:
            slist = []
        services = Services.objects.filter(id=s_id)

        # com = serializers.serialize("json",open_hours)
        
        
        return JsonResponse({'appointment_slots':slist})

class confbook(View):
    def post(self, request):
        data=json.loads(request.body)
        return JsonResponse({'sdata':'It Works'})