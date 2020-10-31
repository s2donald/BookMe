from django.shortcuts import render, get_object_or_404
from account.models import Account
from business.models import Company, Services, OpeningHours, Clients, CompanyReq
from consumer.models import Bookings
from django.http import JsonResponse
from django.views import View
import json
from django.core import serializers
import datetime, pytz
from django.utils import timezone
from account.forms import UpdatePersonalForm, AccountAuthenticationForm
from django.contrib.auth import authenticate, login
from account.tasks import reminderEmail, confirmedEmail, consumerCreatedEmailSent
from businessadmin.tasks import requestToBeClient
# from account.models import Account
# Create your views here.

def get_companyslug(request, slug):
    request.viewing_company = get_object_or_404(Company, slug=slug)

def bookingurl(request):
    user = request.user
    company = request.viewing_company
    services = Services.objects.filter(business=company)
    if user.is_authenticated:
        returnClient = company.clients.filter(user=user,first_name=user.first_name).exists() or company.clients.filter(phone=user.phone,first_name=user.first_name,).exists() or company.clients.filter(email=user.email,first_name=user.first_name).exists()
    else:
        returnClient = False
    return render(request, 'bookingpage/home.html', {'returnClient':returnClient,'user': user, 'company':company, 'services':services})

def bookingServiceView(request, pk):
    user = request.user
    company = request.viewing_company
    service = get_object_or_404(Services, id=pk)
    personal_form = UpdatePersonalForm()
    gibele_form = AccountAuthenticationForm()
    if user.is_authenticated:
        returnClient = company.clients.filter(user=user).exists() or company.clients.filter(phone=user.phone).exists() or company.clients.filter(email=user.email).exists()
    else:
        returnClient = False
    return render(request, 'bookingpage/testBookingPage.html', {'returnClient':returnClient,'user': user, 'company':company, 'service':service, 'personal_form':personal_form, 'gibele_form':gibele_form})

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
        # print(b_open.hour)
        naive = datetime.datetime(year, month, day, b_open.hour, b_open.minute)
        # print(timezone.localtime(timezone.make_aware(naive)))
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
        start = timezone.localtime(timezone.make_aware(start))
        end = timezone.localtime(timezone.make_aware(end))
        if user.is_authenticated:
            if Bookings.objects.filter(company=company, start=start, end=end).count()<1:
                #Check if the user is already a client
                if company.clients.filter(user=user, first_name=user.first_name).exists():
                    guest = company.clients.get(user=user, first_name=user.first_name)
                    guest.last_name = user.last_name
                    guest.email = user.email
                    guest.phone = user.phone
                    guest.save()

                #Check if the client object was already created by the company
                elif company.clients.filter(phone=user.phone, first_name=user.first_name).exists():
                    guest = company.clients.filter(phone=user.phone, first_name=user.first_name).first()
                    guest.user = user
                    guest.email = user.email
                    guest.last_name = user.last_name
                    guest.save()

                elif company.clients.filter(email=user.email, first_name=user.first_name).exists():
                    guest = company.clients.filter(email=user.email, first=user.first_name).first()
                    guest.user = user
                    guest.phone = user.phone
                    guest.last_name = user.last_name
                    guest.save()
                else:
                    guest = Clients.objects.create(company=company, user=user, first_name=user.first_name,last_name=user.last_name,phone=user.phone,email=user.email)
                    guest.save()
                    company.clients.add(guest)
                    company.save()
                booking = Bookings.objects.create(user=user,guest=guest,service=service, company=company,start=start, end=end, price=price)
                booking.save()
                confirmedEmail.delay(booking.id)
                startTime = start - datetime.timedelta(minutes=15)
                reminderEmail.apply_async(args=[booking.id], eta=startTime, task_id=booking.slug)
                good = True
            else:
                good = False
        else:
            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            phone = data['phone']
            if Bookings.objects.filter(company=company, start=start, end=end).count()<1:
                if Account.objects.filter(email=email, is_guest=False).exists():
                    return JsonResponse({'time':time, 's_id':s_id,'start':start,'date':date,'time':time, 'good':good, 'emailerr':'The email you have provided has already been used to create an account. Please sign into Gibele then try booking again later.'})
                
                if Clients.objects.filter(email=email, user=None,first_name=first_name, last_name=last_name,phone=phone, company=company).exists():
                    guest = Clients.objects.get(company=company, email=email, first_name=first_name,last_name=last_name,phone=phone)
                else:
                    guest = Clients.objects.create(company=company,first_name=first_name,last_name=last_name,phone=phone,email=email)
                    guest.save()
                    company.clients.add(guest)
                    company.save()

                booking = Bookings.objects.create(user=user,service=service, company=company,
                                                start=start, end=end, price=price)
                booking.save()

                confirmedEmail.delay(booking.id)
                startTime = start - datetime.timedelta(minutes=15)
                reminderEmail.apply_async(args=[booking.id], eta=startTime)
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
                return JsonResponse({'result':False})
        else:
            return JsonResponse({'result':False})
        
    def get(self, request):
        return JsonResponse({})

class facebookLogin(View):
    def post(self, request):
        return JsonResponse({})

class requestSpot(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(Account, email=request.user.email)
        else:
            return JsonResponse({'data':'You must be signed in. Please try again later'})
        company_id = request.POST.get('company_id')
        company = get_object_or_404(Company, id=company_id)
        requestUser = CompanyReq.objects.filter(user=user, company=company).exists()
        if not requestUser:
            requestUser = CompanyReq.objects.create(user=user, company=company, add_to_list=True)
            requestUser.save()
            requestToBeClient.delay(requestUser.id)
        return JsonResponse({'data':'good'})

class checkIfClientView(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(Account, email=request.user.email)
        else:
            return JsonResponse({'data':"You must be signed in. Please try again later"})
        company_id = request.POST.get('company_id')

        company = get_object_or_404(Company, id=company_id)

        #Check if the user object is on the client list
        requestUser = company.clients.filter(user=user, first_name=user.first_name, company=company).exists()
        if requestUser:
            return JsonResponse({'good':'good'})
            
        #Check if the user email is on the client list
        email = user.email
        requestUser = company.clients.filter(email=email, first_name=user.first_name, company=company).exists()
        if requestUser:
            return JsonResponse({'good':'good'})

        #Check if the users phone number is on the client list
        phone = user.phone
        requestUser = company.clients.filter(phone=phone, first_name=user.first_name, company=company).exists()
        if requestUser:
            return JsonResponse({'good':'good'})

        return JsonResponse({'data':'notclient'})

from django.core.validators import validate_email
from django import forms
class createAccountView(View):
    def post(self, request):
        email = request.POST.get('email')
        first = request.POST.get('first')
        last = request.POST.get('last')
        pw = request.POST.get('password')

        try:
            validate_email(email)
        except forms.ValidationError:
            return JsonResponse({'error':'notanemail'})
        
        if Account.objects.filter(email=email).exists():
            return JsonResponse({'error':'taken'})
        else:
            acct = Account.objects.create_user(email=email,password=pw)
            acct.first_name = first
            acct.last_name=last
            acct.is_consumer=True
            acct.save()
            consumerCreatedEmailSent.delay(acct.id)
            account = authenticate(email=email, password=pw)
            login(request, account)
        return JsonResponse({'good':'good'})

