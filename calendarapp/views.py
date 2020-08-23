from django.shortcuts import render, get_object_or_404
from business.models import Company, Services, OpeningHours
from consumer.models import Bookings
from django.http import JsonResponse
from django.views import View
import json
from django.core import serializers
import datetime
from account.forms import UpdatePersonalForm
# from account.models import Account
# Create your views here.


def get_companyslug(request, slug):
    request.viewing_company = get_object_or_404(Company, slug=slug)

def bookingurl(request):
    user = request.user
    company = request.viewing_company
    services = Services.objects.filter(business=company)
    form = UpdatePersonalForm()
    return render(request, 'bookingpage/home.html', {'user': user, 'company':company, 'services':services, 'personal_form':form})

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
        print(t)

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

        is_auth = request.user.is_authenticated

        if open_hours.is_closed==False:
            slist = list(time_slots(b_open,b_close,interval))
        else:
            slist = []
        services = Services.objects.filter(id=s_id)

        # com = serializers.serialize("json",open_hours)
        
        
        return JsonResponse({'appointment_slots':slist, 'auth':is_auth})

class confbook(View):
    def post(self, request):
        data=json.loads(request.body)
        return JsonResponse({'sdata':'It Works'})

class phoneValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email = data['email']
        phone = data['phone']
        regex= r'^\+?1?\d{9,15}$'
        result = re.match(regex, phone)
        if (request.user.email!=str(email)) and (Account.objects.filter(email=email).exists()):
            return JsonResponse({'email_error':'This email already exists!'}, status=409)
        if not (result):
            return JsonResponse({'phone_error':'Please enter a valid phone number.'}, status=409)
        return JsonResponse({'email_valid':True})

class createAppointment(View):
    def post(self, request):
        data=json.loads(request.body)
        date = data['date']
        time = data['time']
        month = data['month']+1
        day = data['day']
        year = data['year']
        s_id = data['s_id']
        company = request.viewing_company
        user = request.user
        service = get_object_or_404(Services, id=s_id)
        startdate = datetime.datetime(year,month,day)
        starttime = datetime.datetime.strptime(time,'%I:%M %p').time()
        start = datetime.datetime.combine(startdate, starttime)
        end = start + datetime.timedelta(hours=service.duration_hour,minutes=service.duration_minute)
        print(end)
        if user.is_authenticated:
            email = user.email
            first_name = user.first_name
            last_name = user.last_name
            phone = user.phone
            address = user.address
            postal = user.postal
            province = user.province
            city = user.city
            booking = Bookings.objects.create(user=user,first_name=first_name,last_name=last_name,
                                                phone=phone,address=address,postal=postal,
                                                province=province,city=city,service=service, company=company,
                                                start=start, end=end)
            booking.save()
        else:
            email = 'guest@gibele.com'
            user = get_object_or_404(Account,email=email)
            first_name = data['first_name']
            last_name = data['last_name']
            phone = data['phone']
            address = data['address']
            postal = data['postal']
            province = data['province']
            city = data['city']
        return JsonResponse({'time':time, 's_id':s_id,'start':start,'date':date,'time':time})

