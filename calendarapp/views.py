from django.shortcuts import render, get_object_or_404
from account.models import Account
from business.models import Company, Services, OpeningHours, Clients, CompanyReq, Gallary, Category, SubCategory, Amenities
from consumer.models import Bookings, extraInformation, Reviews
from django.db.models import Count
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
import json, urllib
from django.core import serializers
import datetime, pytz
from django.utils import timezone
from account.forms import UpdatePersonalForm, AccountAuthenticationForm, AccountAuthenticationFormId
from django.contrib.auth import authenticate, login
from account.tasks import reminderEmail, confirmedEmail, consumerCreatedEmailSent, confirmedEmailCompany
from businessadmin.tasks import requestToBeClient
from business.forms import VehicleMakeModelForm, AddressForm
import re
from gibele import settings
from django.views.decorators.clickjacking import xframe_options_exempt

# from account.models import Account
# Create your views here.

def get_companyslug(request, slug):
    request.viewing_company = get_object_or_404(Company, slug=slug)

@xframe_options_exempt
def bookingurl(request):
    user = request.user
    company = request.viewing_company
    # services = Services.objects.filter(business=company)
    if user.is_authenticated:
        returnClient = company.clients.filter(user=user,first_name=user.first_name).exists() or company.clients.filter(phone=user.phone,first_name=user.first_name,).exists() or company.clients.filter(email=user.email,first_name=user.first_name).exists()
    else:
        returnClient = False
    address = company.address
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    services = Services.objects.all().filter(business=company)
    reviews = Reviews.objects.filter(company=company).order_by('-created')
    amenities = Amenities.objects.filter(company=company).order_by('amenity')
    sun_hour = OpeningHours.objects.get(company=company, weekday=0)
    mon_hour = OpeningHours.objects.get(company=company, weekday=1)
    tues_hour = OpeningHours.objects.get(company=company, weekday=2)
    wed_hour = OpeningHours.objects.get(company=company, weekday=3)
    thur_hour = OpeningHours.objects.get(company=company, weekday=4)
    fri_hour = OpeningHours.objects.get(company=company, weekday=5)
    sat_hour = OpeningHours.objects.get(company=company, weekday=6)
    galPhotos = Gallary.objects.filter(company=company)
    paginator = Paginator(reviews, 6)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    paginator = Paginator(galPhotos, 6)
    page = request.GET.get('page')
    try:
        galPhotos = paginator.page(page)
    except PageNotAnInteger:
        galPhotos = paginator.page(1)
    except EmptyPage:
        galPhotos = paginator.page(paginator.num_pages)
    return render(request, 'bookingpage/onestaff/bookingpage/homes.html', {'returnClient':returnClient,'user': user, 'page':page,'photos':galPhotos,'sun_hour':sun_hour,'mon_hour':mon_hour,'tues_hour':tues_hour,'wed_hour':wed_hour,'thur_hour':thur_hour,'fri_hour':fri_hour,'sat_hour':sat_hour,'subcategories':subcategories,'amenities':amenities,'address':address,'company':company,'category':category,'categories':categories, 'services':services, 'reviews':reviews})

@xframe_options_exempt
def bookingServiceView(request, pk):
    user = request.user
    company = request.viewing_company
    service = get_object_or_404(Services, id=pk)
    personal_form = UpdatePersonalForm()
    gibele_form = AccountAuthenticationFormId()
    if user.is_authenticated:
        returnClient = company.clients.filter(user=user,first_name=user.first_name).exists() or company.clients.filter(phone=user.phone,first_name=user.first_name,).exists() or company.clients.filter(email=user.email,first_name=user.first_name).exists()
    else:
        returnClient = False
    if company.category.name == 'Automotive Services':
        extra_info_form = VehicleMakeModelForm()
    elif company.category.name == 'Home Services':
        extra_info_form = AddressForm()
    else:
        extra_info_form = AddressForm()
    return render(request, 'bookingpage/onestaff/bookingpage/testBookingPage.html', {'extra_info_form':extra_info_form,'returnClient':returnClient,'user': user, 'company':company, 'service':service, 'personal_form':personal_form, 'gibele_form':gibele_form})

def time_slots(start_time, end_time, interval, duration_hour, duration_minute, year, month, day, company, staff_breaks):
    t = start_time
    servDate = timezone.localtime(timezone.make_aware(datetime.datetime(year,month,day)))
    if timezone.localtime(timezone.now()).date() == servDate.date():
        while timezone.localtime(timezone.now()).time()>t:
            t = timezone.localtime(timezone.make_aware(datetime.datetime.combine(datetime.date.today(), t) +
             datetime.timedelta(minutes=interval))).time()
    availableDay = []
    while t < end_time:
        servStart = timezone.localtime(timezone.make_aware(datetime.datetime.combine(servDate, t)))
        endTime = timezone.localtime(timezone.make_aware(datetime.datetime.combine(servDate, t) + datetime.timedelta(hours=duration_hour,minutes=duration_minute)))
        objects = Bookings.objects.filter(company=company, start__gte=servDate, end__lte=timezone.localtime(servDate + datetime.timedelta(days=1)), is_cancelled_user=False, is_cancelled_company=False)
        # objlength = len(objects)
        count = 0
        if endTime.time() <= t:
            endTime = timezone.localtime(timezone.make_aware(datetime.datetime.combine(servDate, datetime.time(23,59,59))))
        for obj in objects:
            #Check if the booking date from the loop is the same as the requested date
            if (timezone.localtime(obj.start).date() == timezone.localtime(servStart).date()):
                #Check the buffer option that applies to this booking
                # buffer = obj.service.padding
                before_durhour = 0
                before_durmin =0
                after_durhour = 0
                after_durmin = 0
                # if buffer == 'bf':
                #     before_durhour = obj.service.paddingtime_hour
                #     before_durmin = obj.service.paddingtime_minute
                #     after_durhour = obj.service.paddingtime_hour
                #     after_durmin = obj.service.paddingtime_minute
                # elif buffer == 'before':
                #     before_durhour = obj.service.paddingtime_hour
                #     before_durmin = obj.service.paddingtime_minute
                # elif buffer == 'after':
                #     after_durhour = obj.service.paddingtime_hour
                #     after_durmin = obj.service.paddingtime_minute
                #The start time of the already booked service
                s = timezone.localtime(obj.start).time()
                #The endtime of the already booked service
                g = timezone.localtime(obj.end).time()
                #Check if already booked service interfers with the proposed 
                if((s<=servStart.time()<g) or (s<endTime.time()<g) or (end_time<endTime.time())):
                    t = endTime.time()
                    #Since we know this booking time falls between an already booked service 
                    # We basically check if the ending time of the booking interval 't' is less than the booking time of the 
                    # already booked service. If it is then we use that time 'g' to start the new interval.
                    if(t<g):
                        t=g
                    count = 1
        if not objects:
            if end_time<endTime.time():
                t = endTime.time()
                count = 1
        if count == 0:
            for breaks in staff_breaks:
                if((breaks.from_hour<=servStart.time()<breaks.to_hour) or (breaks.from_hour<endTime.time()<breaks.to_hour)):
                    count = 1
                    t=breaks.to_hour
                print(t)

        if count==0:
            availableDay.append(t.strftime("%I:%M %p"))
            t = timezone.localtime(timezone.make_aware(datetime.datetime.combine(datetime.date.today(), t) +
                datetime.timedelta(minutes=interval))).time()
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
        # timezone.localtime(timezone.make_aware(naive))
        interval= company.interval
        duration_hour = Services.objects.get(pk=s_id).duration_hour
        duration_minute = Services.objects.get(pk=s_id).duration_minute
        #Check buffer before and after
        # beforeafter = Services.objects.get(pk=s_id).padding
        # buffer_durhour = Services.objects.get(pk=s_id).paddingtime_hour
        # buffer_durmin = Services.objects.get(pk=s_id).paddingtime_minute
        is_auth = request.user.is_authenticated

        # #This code has to change once staff members are added
        if company.staffmembers.count() == 1:
            breakss = company.staffmembers.all()[0].staff_breaks.all()
        else:
            breakss = None
        staff_breaks = []
        if breakss:
            for breaks in breakss:
                if weekday == breaks.weekday:
                    staff_breaks.append(breaks)

        # #This code has to change once staff members are added
        # for staffmem in company.staffmembers.all():
        #     staff_break = staffmem.staff_breaks.all()
        
        if open_hours.is_closed==False:
            slist = list(time_slots(b_open,b_close,interval, duration_hour, duration_minute, year, month, day, company, staff_breaks))
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


def checkRecaptcha(self, request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
            
    if result['success']:
        return True
    else:
        return False

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
            if company.returning:
                if company.clients.filter(user=user, first_name=user.first_name).exists():
                    pass
                #Check if the client object was already created by the company
                elif company.clients.filter(phone=user.phone, first_name=user.first_name).exists():
                    pass
                elif company.clients.filter(email=user.email, first_name=user.first_name).exists():
                    pass
                else:
                    return JsonResponse({'time':time, 's_id':s_id,'start':start,'date':date,'time':time, 'emailerr':True, 'notonclientlist':True})
            if Bookings.objects.filter(company=company, start=start, end=end, is_cancelled_user=False,is_cancelled_company=False).count()<1:
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
                if company.category.name == 'Automotive Services':
                    make = data['vehmake']
                    model = data['vehmodel']
                    vehyear = data['vehyear']
                    extraInformation.objects.create(car_make=make, car_model=model, car_year=vehyear, booking=booking)

                confirmedEmail.delay(booking.id)
                confirmedEmailCompany.delay(booking.id)
                confirmtime = 30
                if service.checkintime:
                    confirmtime = service.checkintime + 30
                startTime = timezone.localtime(start - datetime.timedelta(minutes=confirmtime))
                reminderEmail.apply_async(args=[booking.id], eta=startTime, task_id=booking.slug)
                good = True
            else:
                good = False
        else:
            email = data['email']
            first_name = data['first_name']
            last_name = data['last_name']
            phone = data['phone']
            if company.returning:
                return JsonResponse({'time':time, 's_id':s_id,'start':start,'date':date,'time':time, 'emailerr':True, 'notonclientlist':True})
            if Bookings.objects.filter(company=company, start=start, end=end, is_cancelled_user=False,is_cancelled_company=False).count()<1:
                if Account.objects.filter(email=email).exists():
                    return JsonResponse({'time':time, 's_id':s_id,'start':start,'date':date,'time':time, 'good':False, 'emailerr':'The email you have provided has already been used to create an account. Please sign into Gibele then try booking again later.'})
                
                if Clients.objects.filter(email=email, user=None,first_name=first_name, last_name=last_name,phone=phone, company=company).exists():
                    guest = Clients.objects.get(company=company, email=email, first_name=first_name,last_name=last_name,phone=phone)
                else:
                    guest = Clients.objects.create(company=company,first_name=first_name,last_name=last_name,phone=phone,email=email)
                    guest.save()
                    company.clients.add(guest)
                    company.save()

                booking = Bookings.objects.create(guest=guest,service=service, company=company,
                                                start=start, end=end, price=price)
                booking.save()
                if company.category.name == 'Automotive Services':
                    make = data['vehmake']
                    model = data['vehmodel']
                    vehyear = data['vehyear']
                    extraInformation.objects.create(car_make=make, car_model=model, car_year=vehyear, booking=booking)
                    
                if email:
                    confirmedEmail.delay(booking.id)
                    confirmedEmailCompany.delay(booking.id)
                    confirmtime = 30
                    if service.checkintime:
                        confirmtime = service.checkintime + 30
                    startTime = start - datetime.timedelta(minutes=confirmtime)
                    reminderEmail.apply_async(args=[booking.id], eta=startTime)
                good = True
            else:
                good = False

        return JsonResponse({'time':time, 's_id':s_id,'start':start,'date':date,'time':time, 'good':good})

class LoginView(View):
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        recaptcha_response = request.POST.get('g-recaptcha-response','')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        result['success'] = True
        if result['success']:
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'result':True})
                else:
                    return JsonResponse({'result':False})
            else:
                return JsonResponse({'result':False})
        else:
            return JsonResponse({'recaptcha':False})
        
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
        password = request.POST.get('password')
        # calculating the length
        length_error = len(password) < 8
        # searching for digits
        digit_error = re.search(r"\d", password) is None
        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None
        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None
        # searching for symbols
        symbol_error = re.search(r"[ !#?<>:$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
        # overall result
        password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )
        try:
            validate_email(email)
        except forms.ValidationError:
            return JsonResponse({'error':'notanemail'})
        
        if Account.objects.filter(email=email).exists():
            return JsonResponse({'error':'taken'})
        elif not password_ok:
            return JsonResponse({'error':'notgoodpass'})
        else:
            acct = Account.objects.create_user(email=email,password=password)
            acct.first_name = first
            acct.last_name=last
            acct.is_consumer=True
            acct.save()
            consumerCreatedEmailSent.delay(acct.id)
            account = authenticate(email=email, password=password)
            login(request, account)
        return JsonResponse({'good':'good'})


# def bookingStaffUrl(request, slug):
    

