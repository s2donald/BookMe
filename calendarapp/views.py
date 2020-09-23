from django.shortcuts import render, get_object_or_404
from account.models import Account, Guest
from business.models import Company, Services, OpeningHours
from consumer.models import Bookings
from django.http import JsonResponse
from django.views import View
import json
from django.core import serializers
import datetime, pytz
from account.forms import UpdatePersonalForm, AccountAuthenticationForm
from django.contrib.auth import authenticate, login
# from account.models import Account
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
    personal_form = UpdatePersonalForm()
    gibele_form = AccountAuthenticationForm()
    return render(request, 'bookingpage/indservice.html', {'user': user, 'company':company, 'service':service, 'personal_form':personal_form, 'gibele_form':gibele_form})

def time_slots(start_time, end_time, interval, duration_hour, duration_minute, year, month, day, company):
    t = start_time
    servDate = datetime.datetime(year,month,day).astimezone(pytz.timezone("UTC"))
    availableDay = []
    while t < end_time:
        begTime = t
        servStart = datetime.datetime.combine(servDate, t).astimezone(pytz.timezone("UTC"))
        endTime = (datetime.datetime.combine(servDate, t) +
                    datetime.timedelta(hours=duration_hour,minutes=duration_minute)).astimezone(pytz.timezone("UTC"))
        objects = Bookings.objects.filter(company=company)
        objlength = len(objects)
        count = 0
        for i in range(objlength):
            if (objects[i].start.date() == servStart.date()):
                s = objects[i].start.time()
                g = objects[i].end.time()
                if((servStart.time()<=s<endTime.time()) or (servStart.time()<g<endTime.time())):
                    count = 1
        if count==0:
            availableDay.append(t.strftime("%I:%M %p"))
        t = (datetime.datetime.combine(datetime.date.today(), t) +
             datetime.timedelta(minutes=interval)).time()
    return availableDay

class bookingTimes(View):
    def post(self, request):
        data=json.loads(request.body)
        s_id = data['id']
        month = data['month']+1
        year = data['year']
        day = data['day']
        weekday = data['weekday']
        date=data['date']
        company = request.viewing_company
        open_hours = get_object_or_404(OpeningHours,company=company, weekday=weekday)
        #We need to add the service time and validate whether the service can be fit in the timeslot
        b_open = open_hours.from_hour
        b_close = open_hours.to_hour
        interval= company.interval
        duration_hour = Services.objects.get(pk=s_id).duration_hour
        duration_minute = Services.objects.get(pk=s_id).duration_minute
        is_auth = request.user.is_authenticated

        if open_hours.is_closed==False:
            slist = list(time_slots(b_open,b_close,interval, duration_hour, duration_minute, year, month, day, company))
            # appslot = list(appointmentValid(slist, duration_hour, duration_minute, len(slist)))
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
        price = service.price
        startdate = datetime.datetime(year,month,day)
        starttime = datetime.datetime.strptime(time,'%I:%M %p').time()
        start = datetime.datetime.combine(startdate, starttime)
        end = start + datetime.timedelta(hours=service.duration_hour,minutes=service.duration_minute)
        if user.is_authenticated:
            print(user)
            # email = user.email
            # first_name = user.first_name
            # last_name = user.last_name
            # phone = user.phone
            # address = user.address
            # postal = user.postal
            # province = user.province
            # city = user.city
            if Bookings.objects.filter(company=company, start=start, end=end).count()<1:
                booking = Bookings.objects.create(user=user,service=service, company=company,
                                                start=start, end=end, price=price)
                booking.save()
                good = True
            else:
                good = False
        else:
            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            phone = data['phone']
            guest = Guest.objects.create(first_name=first_name,last_name=last_name,phone=phone,email=email)
            guest.save()
            if Bookings.objects.filter(company=company, start=start, end=end).count()<1:
                booking = Bookings.objects.create(guest=guest,service=service, company=company,
                                                start=start, end=end, price=price)
                booking.save()
                company.guest_client.add(guest)
                company.save()
                good = True
            else:
                good = False

        return JsonResponse({'time':time, 's_id':s_id,'start':start,'date':date,'time':time, 'good':good})

class LoginView(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'result':True})
            else:
                print('hello')
                return JsonResponse({'result':False})
        else:
            return JsonResponse({'result':False})
        
    def get(self, request):
        return JsonResponse({})

