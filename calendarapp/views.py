from django.shortcuts import render, get_object_or_404
from account.models import Account
from account.forms import ConsumerRegistrationForm
from business.models import Company, Services, OpeningHours, Clients, CompanyReq, Gallary, Category, SubCategory, Amenities
from businessadmin.models import StaffWorkingHours, StaffMember, Breaks
from consumer.models import Bookings, extraInformation, Reviews
from .models import bookingForm
from django.db.models import Count
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
import json, urllib
from django.core import serializers
import datetime, pytz
from django.utils import timezone
from account.forms import UpdatePersonalForm, AccountAuthenticationForm, AccountAuthenticationFormId,GuestPersonalForm
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from django import forms
from account.tasks import reminderEmail, emailRequestServiceCompany, confirmedEmail, consumerCreatedEmailSent, confirmedEmailCompany, send_sms_reminder_client, send_sms_confirmed_client, emailRequestServiceClient, send_sms_requestService_company, send_sms_requestService_client
from businessadmin.tasks import requestToBeClient
from business.forms import VehicleMakeModelForm, AddressForm
import re
from gibele import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.loader import render_to_string
import multiprocessing
from dateutil.relativedelta import relativedelta
# from account.models import Account
# Create your views here.

def get_companyslug(request, slug):
    request.viewing_company = get_object_or_404(Company, slug=slug)

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

from django.db.models import Q
def time_slots(start_time, end_time, interval, duration_hour, duration_minute, year, month, day, company, staff_breaks, staff):
    t = start_time
    servDate = timezone.localtime(timezone.make_aware(datetime.datetime(year,month,day)))
    dateWindowBefore = timezone.localtime(timezone.now()) + datetime.timedelta(days=company.before_window_day,hours=company.before_window_hour,minutes=company.before_window_min)
    dateWindowAfter = timezone.localtime(timezone.now()) + relativedelta(days=company.after_window_day,months=company.after_window_month)

    #We check if the date they are looking to book an appointment is today. If so, we get the earliest available time
    if timezone.localtime(timezone.now()).date() == servDate.date():
        init_time = timezone.localtime(timezone.now() + datetime.timedelta(hours=company.before_window_hour, minutes=company.before_window_min)).time()
        while init_time>t:
            t = timezone.localtime(timezone.make_aware(datetime.datetime.combine(datetime.date.today(), t) +
             datetime.timedelta(minutes=interval))).time()
    availableDay = []
    #end_time is the closing hour of the shop
    while t < end_time:
        servStart = timezone.localtime(timezone.make_aware(datetime.datetime.combine(servDate, t)))
        endTime = timezone.localtime(timezone.make_aware(datetime.datetime.combine(servDate, t) + datetime.timedelta(hours=duration_hour,minutes=duration_minute)))
        objects = staff.staff_bookings.filter(company=company, start__gte=servDate, is_cancelled_user=False, is_cancelled_company=False, is_cancelled_request=False)
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
                s = timezone.localtime(obj.start)
                #The endtime of the already booked service
                g = timezone.localtime(obj.end)
                #Check if already booked service interfers with the proposed 
                if((s<=servStart<g) or (s<endTime<g) or (end_time<endTime.time())):
                    t = endTime.time()
                    #Since we know this booking time falls between an already booked service 
                    # We basically check if the ending time of the booking interval 't' is less than the booking time of the 
                    # already booked service. If it is then we use that time 'g' to start the new interval.
                    if(t<g.time()):
                        t=g.time()
                    count = 1
                
        if not objects:
            if end_time<endTime.time():
                t = endTime.time()
                count = 1

        if count == 0:
            for breaks in staff_breaks:
                if((servStart.time()<=breaks.from_hour<endTime.time()) or (servStart.time()<breaks.to_hour<endTime.time())):
                    count = 1
                    t=breaks.to_hour

        if count==0:
            availableDay.append(t)
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
            slist = list(time_slots(b_open,b_close,interval, duration_hour, duration_minute, year, month, day, company, staff_breaks, staff))
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

class loadSignUpForm(View):
    def post(self, request):
        company = request.viewing_company
        print(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if not (password == pass2):
            return JsonResponse({'error':'passnotsame'})
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
            acct.first_name = first_name
            acct.last_name= last_name
            acct.is_consumer=True
            acct.save()
            consumerCreatedEmailSent.delay(acct.id)
            account = authenticate(email=email, password=password)
            service_id = request.session.get('service_id')
            login(request, account)
            request.session['service_id'] = service_id
            html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/bookingRequest.html', {'company':company}, request)
            return JsonResponse({'html_content':html, 'loggedinuser':True})
    def get(self, request):
        company = request.viewing_company
        reg_form = ConsumerRegistrationForm()
        html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/login/returningguest.html', {'company':company, 'reg_form':reg_form}, request)
        return JsonResponse({'html_content':html, 'loggedinuser':True})

class loadLoginFormRequest(View):
    def get(self, request):
        company = request.viewing_company
        account_form = AccountAuthenticationForm()
        reg_form = ConsumerRegistrationForm()
        html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/login/returnClient.html', {'company':company, 'account_form':account_form, 'reg_form':reg_form}, request)
        return JsonResponse({'html_content':html, 'loggedinuser':True})


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

def bookingurlupdated(request):
    user = request.user
    company = request.viewing_company
    dateWindowBefore = timezone.localtime(timezone.now()) + datetime.timedelta(days=company.before_window_day,hours=company.before_window_hour,minutes=company.before_window_min)
    dateWindowAfter = timezone.localtime(timezone.now()) + relativedelta(days=company.after_window_day,months=company.after_window_month)
    kanalytics = request.GET.get('k')
    if kanalytics:
        print(company.company_views.kijiji)
        # k = company.company_views.kijiji
        # k += 1
        # k.save()

    print(kanalytics)
    if company.business_type == 'product':
        return render(request, 'productspage/productpage.html',{'user':user,'company':company, 'dateWindowBefore':dateWindowBefore, 'dateWindowAfter':dateWindowAfter})
    else:
        return render(request, 'bookingpage/multiplestaff/bookingpage/bookingpage.html',{'user':user,'company':company, 'dateWindowBefore':dateWindowBefore, 'dateWindowAfter':dateWindowAfter})

def bookingStaffUrl(request, slug):
    user = request.user
    company = request.viewing_company
    return render(request, 'bookingpage/onestaff/bookingpage/homes.html',{'user':user,'company':company})

class staffofferingservice(View):
    def post(self, request):
        # handle login or create account
        pass
    def get(self, request):
        company = request.viewing_company
        service_id = request.GET.get('service_id')
        request.session['service_id'] = service_id
        service = Services.objects.get(pk=service_id)
        staff = company.staffmembers.filter(services=service)
        user=request.user
        if company.returning:
            if not user.is_authenticated:
                account_form = AccountAuthenticationForm()
                html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/login/returnClient.html', {'account_form':account_form, 'company':company, 'service':service}, request)
                return JsonResponse({'html_content':html, 'returning':True})
            elif company.clients.filter(user=user, first_name=user.first_name).exists():
                pass
            #Check if the client object was already created by the company
            elif company.clients.filter(phone=user.phone, first_name=user.first_name).exists():
                pass
            elif company.clients.filter(email=user.email, first_name=user.first_name).exists():
                pass
            else:
                html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/bookingRequest.html', {'company':company, 'service':service}, request)
                return JsonResponse({'html_content':html, 'returning':True})
        if user.is_authenticated:
            html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/services_offered_staff.html', {'company':company,'staff':staff, 'service':service}, request)
        else:
            html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/services_offered_staff.html', {'company':company,'staff':staff, 'service':service}, request)
        return JsonResponse({'html_content':html})

class bookingTimesView(View):
    def get(self, request):
        service_id = request.session.get('service_id')
        company = request.viewing_company
        staff_id = request.GET.get('staff_id')
        request.session['staff_id'] = staff_id
        service = Services.objects.get(pk=service_id)
        staff = company.staffmembers.filter(services=service)
        staffmem = StaffMember.objects.get(pk=staff_id)
        html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/bookingCalendar.html', {'company':company,'staff':staffmem, 'service':service}, request)
        hours = render_to_string('bookingpage/multiplestaff/bookingpage/partials/staff/staff_hours.html', {'staff':staffmem}, request)
        info = render_to_string('bookingpage/multiplestaff/bookingpage/partials/staff/staff_information.html', {'staff':staffmem}, request)
        return JsonResponse({'html_content':html, 'hours_content':hours, 'info_content':info, 'service_id':service_id})


class bookingCalendarRender(View):
    def get(self, request):
        company = request.viewing_company
        s_id = int(request.GET.get('service_id'))
        staff_id = int(request.GET.get('staff_id'))
        month = int(request.GET.get('month'))+1
        year = int(request.GET.get('year'))
        day = int(request.GET.get('day'))
        weekday = int(request.GET.get('weekday'))
        staff = StaffMember.objects.get(pk=staff_id)
        staff_hours = staff.staff_hours.get(weekday=weekday)

        #We need to add the service time and validate whether the service can be fit in the timeslot
        b_open = staff_hours.from_hour
        b_close = staff_hours.to_hour
        # print(b_open.hour)
        naive = datetime.datetime(year, month, day, b_open.hour, b_open.minute)
        interval= company.interval
        duration_hour = Services.objects.get(pk=s_id).duration_hour
        duration_minute = Services.objects.get(pk=s_id).duration_minute
        is_auth = request.user.is_authenticated

        # #This code has to change once staff members are added
        breakss = staff.staff_breaks.all()
        
        staff_breaks = []
        if breakss:
            for breaks in breakss:
                if weekday == breaks.weekday:
                    staff_breaks.append(breaks)
        if staff_hours.is_off==False:
            slist = list(time_slots(b_open,b_close,interval, duration_hour, duration_minute, year, month, day, company, staff_breaks, staff))
        else:
            slist = []
        service = Services.objects.get(id=s_id)
        html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/bookingtimes/bookingtimes.html', {'list':slist,'staff':staff,'service':service, 'month':month, 'year':year, 'day':day}, request)
        return JsonResponse({'html_content':html_content, 'auth':is_auth})

class confirmationMessageRender(View):
    def get(self, request):
        company = request.viewing_company
        s_id = request.session.get('service_id')
        staff_id = request.session.get('staff_id')
        # s_id = int(request.GET.get('service_id'))
        # staff_id = int(request.GET.get('staff_id'))
        time = request.GET.get('time')
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
        day = int(request.GET.get('day'))
        request.session['time'] = time
        request.session['month'] = month
        request.session['year'] = year
        request.session['day'] = day
        date = datetime.datetime(year, month, day)

        staff = StaffMember.objects.get(pk=staff_id)
        service = Services.objects.get(pk=s_id)
        html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmation.html', {'company':company,'staff':staff,'service':service, 'date':date, 'time':time, 'month':month, 'year':year, 'day':day }, request)
        conf_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/confirmationside.html', {'company':company,'service':service, 'staff':staff }, request)

        return JsonResponse({'html_content':html_content, 'conf_content':conf_content})

    def post(self, request):
        user = request.user
        company = request.viewing_company
        s_id = request.session.get('service_id')
        staff_id = request.session.get('staff_id')
        month = request.session.get('month')
        year = request.session.get('year')
        day = request.session.get('day')
        time = request.session.get('time')
        if company.category.name == 'Automotive Services':
            make = request.POST.get('make')
            model = request.POST.get('model')
            vehyear = request.POST.get('vehyear')
            trim = request.POST.get('trim')
            request.session['vehmake'] = make.replace('%20',' ').replace('%28','(').replace('%29',')')
            request.session['vehmodel'] = model.replace('%20',' ').replace('%28','(').replace('%29',')')
            request.session['vehyear'] = vehyear.replace('%20',' ').replace('%28','(').replace('%29',')')
            request.session['vehtrim'] = trim.replace('%20',' ').replace('%28','(').replace('%29',')')
        

        starttime = datetime.datetime.strptime(time,'%I:%M %p').time()
        startdate = datetime.datetime(year, month, day)
        date = datetime.date(year, month, day)
        staff = get_object_or_404(StaffMember, id=staff_id)
        service = get_object_or_404(Services, id=s_id)
        bookinglist = []
        for newformfield in service.service_forms.all():
            fieldname = request.POST.get(str(newformfield.id)).replace('%20',' ').replace('%28','(').replace('%29',')')
            label = newformfield.label
            bookinglist.append([fieldname, label])
        request.session['formlist'] = bookinglist
        if not user.is_authenticated:
            # render out the login and user form retrieval
            personal_form = GuestPersonalForm(initial={'phone_code':"CA"})
            html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/login/guest.html', {'company':company,'staff':staff,'service':service, 'date':date, 'time':time, 'month':month, 'year':year, 'day':day, 'personal_form':personal_form }, request)
            return JsonResponse({'html_content':html_content, 'notauthenticated':True})
        
        price = service.price
        
        start = datetime.datetime.combine(startdate, starttime)
        end = start + datetime.timedelta(hours=service.duration_hour,minutes=service.duration_minute)
        start = timezone.localtime(timezone.make_aware(start))
        end = timezone.localtime(timezone.make_aware(end))
        
        #Validate the issues first
        if company.returning:
            if company.clients.filter(user=user, first_name=user.first_name).exists():
                pass
            #Check if the client object was already created by the company
            elif company.clients.filter(phone=user.phone, first_name=user.first_name).exists():
                pass
            elif company.clients.filter(email=user.email, first_name=user.first_name).exists():
                pass
            else:
                return JsonResponse({'notonclientlist':True})
        lock = multiprocessing.Lock()
        lock.acquire()
        bcount = Bookings.objects.filter(company=company, staffmem=staff, start__gte=start, end__lte=end, is_cancelled_user=False,is_cancelled_company=False,is_cancelled_request=False).count()
        if bcount<1:
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
            booking = Bookings.objects.create(user=user,guest=guest,service=service, staffmem=staff, company=company,start=start, end=end, price=price)
            booking.save()
            if company.category.name == 'Automotive Services':
                bookinform1 = bookingForm.objects.create(booking=booking, label='Vehicle Year', text=vehyear.replace('%20',' '))
                bookinform2 = bookingForm.objects.create(booking=booking, label='Vehicle Make', text=make.replace('%20',' '))
                bookinform3 = bookingForm.objects.create(booking=booking, label='Vehicle Model', text=model.replace('%20',' '))
                bookinform4 = bookingForm.objects.create(booking=booking, label='Vehicle Trim', text=trim.replace('%20',' '))
                bookinform1.save()
                bookinform2.save()
                bookinform3.save()
                bookinform4.save()
            
            for newformfield in bookinglist:
                bookinform = bookingForm.objects.create(booking=booking, label=newformfield[1], text=newformfield[0])
                bookinform.save()
            # saveformhere

            if service.request:
                reqc = CompanyReq.objects.create(user=user, guest=guest, company=company, is_addbooking=True)
                booking.bookingreq = reqc
                booking.save()
                #Send request sent and recieved to customer and client respectively
                #Email
                emailRequestServiceClient.delay(booking.id)
                emailRequestServiceCompany.delay(booking.id)
                #Text
                if company.subscriptionplan >= 1:
                    send_sms_requestService_company.delay(booking.id)
                    send_sms_requestService_client.delay(booking.id)
                html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/requestServiceSent.html', {'company':company,'staff':staff,'booking':booking }, request)
            else:
                #Send conf and reminder emails
                confirmedEmail.delay(booking.id)
                confirmedEmailCompany.delay(booking.id)
                confirmtime = 30
                if service.checkintime:
                    confirmtime = service.checkintime + 30
                startTime = timezone.localtime(start - datetime.timedelta(minutes=confirmtime))
                reminderEmail.apply_async(args=[booking.id], eta=startTime, task_id=booking.slug)
                # Confirm the appointment through texts with the client
                if company.subscriptionplan >= 1:
                    send_sms_confirmed_client.delay(booking.id)
                    send_sms_reminder_client.apply_async(args=[booking.id], eta=startTime)
                html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/bookingset.html', {'company':company,'staff':staff,'service':service, 'date':date, 'time':time, 'month':month, 'year':year, 'day':day }, request)
        else:
            html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/bookingerror.html', {'company':company,'staff':staff,'service':service, 'date':date, 'time':time, 'month':month, 'year':year, 'day':day }, request)
        lock.release()
        return JsonResponse({'html_content':html_content})

from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, MultiWidgetField, Div, Row

def guestformlayout(staff_id, s_id, time, month, year, day, date):
    newstr = time.split()
    
    return Layout(
                Div(
                    HTML("<h3>Submit Your Info</h3>"),
                    Div(
                        Div(
                            Div(
                                Field('first_name'),
                                css_class='col-md-6 py-0'
                            ),
                            Div(
                                Field('last_name'),
                                css_class='col-md-6 py-0'
                            ),
                            Div(
                                Field('email'),
                                css_class='col-md-6 py-0'
                            ),
                            Div(
                                HTML("<label>Phone Number</label>"),
                                Div(
                                    Div(
                                        Field('phone_code'),
                                        css_class='col-3 p-0 my-2'
                                    ),
                                    Div(
                                        Field('phone'),
                                        css_class='col-9 p-0'
                                    ),
                                    css_class='row p-0'
                                ),
                                css_class='col-md-6 py-0'
                            ),
                            css_class='row py-3',
                        ),
                    ),
                    HTML('<div class="col-md-12" id="subbtndiv"><button id="submitform" data-staff='+ str(staff_id)+' data-service='+ str(s_id)+' data-month='+ str(month)+' data-day='+ str(day) +' data-year='+ str(year) +' data-time="'+ time +'" type="submit" data-sitekey="6LeimeAZAAAAAE119rtvZivK4DW9csX6QhEo5Yla"  data-callback="onSubmit" data-action="submit" class="g-recaptcha btn btn-outline-primary subbtn">Book as a guest</button></div>'),
                    HTML('<div class="col-md-12"><button id="loginGibeleForm" data-staff='+ str(staff_id)+' data-service='+ str(s_id)+' data-month='+ str(month)+' data-day='+ str(day) +' data-year='+ str(year) +' data-time="'+ time +'" type="button" class="btn btn-pill btn-warning accountbtn">Log into BookMe</button></div>'),
                    id="guestform"
                ),

            )

class guestNewFormRender(View):
    def get(self, request):
        company=request.viewing_company
        s_id = request.session.get('service_id')
        staff_id = request.session.get('staff_id')
        month = request.session.get('month')
        year = request.session.get('year')
        day = request.session.get('day')
        time = request.session.get('time')
        staff = get_object_or_404(StaffMember, id=staff_id)
        service = get_object_or_404(Services, id=s_id)
        date = datetime.date(year, month, day)
        personal_form = GuestPersonalForm(initial={'phone_code':"CA"})
        html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/login/guest.html', {'company':company,'staff':staff,'service':service, 'date':date, 'time':time, 'month':month, 'year':year, 'day':day, 'personal_form':personal_form }, request)
        return JsonResponse({'html_content':html_content, 'notauthenticated':True})

class guestFormRender(View):
    def post(self, request):
        company=request.viewing_company
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        personal_form = GuestPersonalForm(request.POST)

        s_id = request.session.get('service_id')
        staff_id = request.session.get('staff_id')
        month = request.session.get('month')
        year = request.session.get('year')
        day = request.session.get('day')
        time = request.session.get('time')
        make = request.session.get('vehmake')
        model = request.session.get('vehmodel')
        vehyear = request.session.get('vehyear')
        trim = request.session.get('vehtrim')
        bookinglist = request.session.get('formlist')

        # staff_id = int(request.POST.get('staff_id'))
        # s_id = int(request.POST.get('service_id'))
        # time = request.POST.get('time')
        # month = int(request.POST.get('month'))
        # year = int(request.POST.get('year'))
        # day = int(request.POST.get('day'))
        # make = request.POST.get('make')
        # model = request.POST.get('model')
        # vehyear = request.POST.get('vehyear')
        # trim = request.POST.get('trim')
        date = datetime.date(year, month, day)
        service = Services.objects.get(pk=s_id)
        staff=StaffMember.objects.get(company=company, pk=staff_id)
        if not personal_form.is_valid():
            error = personal_form.errors.as_json()
            ctx = {}
            ctx.update(csrf(request))
            personal_form.helper.layout = guestformlayout(staff_id, s_id, time, month, year, day, date)
            form_html = render_crispy_form(personal_form, context=ctx)
            return JsonResponse({'form_is_invalid':True,'form_errors':error, 'form_html': form_html})
        else:
            price = service.price
            startdate = datetime.datetime(year,month,day)
            starttime = datetime.datetime.strptime(time,'%I:%M %p').time()
            start = datetime.datetime.combine(startdate, starttime)
            end = start + datetime.timedelta(hours=service.duration_hour,minutes=service.duration_minute)
            start = timezone.localtime(timezone.make_aware(start))
            end = timezone.localtime(timezone.make_aware(end))
            if company.returning:
                html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/bookingReturningClient.html', {'company':company,'staff':staff,'service':service, 'date':date, 'time':time, 'month':month, 'year':year, 'day':day }, request)
                return JsonResponse({'notonclientlist':True, 'html_content':html_content})
            lock = multiprocessing.Lock()
            lock.acquire()
            if Bookings.objects.filter(company=company, staffmem=staff, start__gte=start, end__lte=end, is_cancelled_user=False,is_cancelled_company=False, is_cancelled_request=False).count()<1:
                if Account.objects.filter(email=email).exists():
                    return JsonResponse({'time':time, 's_id':s_id,'start':start,'date':date,'time':time, 'good':False, 'emailerr':'The email you have provided has already been used to create an account. Please sign into BookMe then try booking again later.'})
                
                if Clients.objects.filter(email=email, user=None,first_name=first_name, last_name=last_name,phone=phone, company=company).exists():
                    guest = Clients.objects.get(company=company, email=email, first_name=first_name,last_name=last_name,phone=phone)
                else:
                    guest = Clients.objects.create(company=company,first_name=first_name,last_name=last_name,phone=phone,email=email)
                    guest.save()
                    company.clients.add(guest)
                    company.save()

                booking = Bookings.objects.create(guest=guest,service=service, company=company,staffmem=staff, start=start, end=end, price=price)
                booking.save()

                if company.category.name == 'Automotive Services':
                    bookinform1 = bookingForm.objects.create(booking=booking, label='Vehicle Year', text=vehyear.replace('%20',' '))
                    bookinform2 = bookingForm.objects.create(booking=booking, label='Vehicle Make', text=make.replace('%20',' '))
                    bookinform3 = bookingForm.objects.create(booking=booking, label='Vehicle Model', text=model.replace('%20',' '))
                    bookinform4 = bookingForm.objects.create(booking=booking, label='Vehicle Trim', text=trim.replace('%20',' '))
                    bookinform1.save()
                    bookinform2.save()
                    bookinform3.save()
                    bookinform4.save()
                
                for newformfield in bookinglist:
                    bookinform = bookingForm.objects.create(booking=booking, label=newformfield[1], text=newformfield[0])
                    bookinform.save()
                
                if service.request:
                    reqc = CompanyReq.objects.create(guest=guest, company=company, is_addbooking=True)
                    booking.bookingreq = reqc
                    booking.save()
                    #Send request sent and recieved to customer and client respectively
                    #Email
                    emailRequestServiceClient.delay(booking.id)
                    emailRequestServiceCompany.delay(booking.id)
                    #Text
                    if company.subscriptionplan >= 1:
                        send_sms_requestService_company.delay(booking.id)
                        send_sms_requestService_client.delay(booking.id)
                    html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/requestServiceSent.html', {'company':company,'staff':staff,'booking':booking }, request)
                else:
                    #Send conf and reminder emails
                    confirmedEmail.delay(booking.id)
                    confirmedEmailCompany.delay(booking.id)
                    confirmtime = 30
                    if service.checkintime:
                        confirmtime = service.checkintime + 30
                    startTime = timezone.localtime(start - datetime.timedelta(minutes=confirmtime))
                    reminderEmail.apply_async(args=[booking.id], eta=startTime, task_id=booking.slug)
                    # Confirm the appointment through texts with the client
                    if company.subscriptionplan >= 1:
                        send_sms_confirmed_client.delay(booking.id)
                        send_sms_reminder_client.apply_async(args=[booking.id], eta=startTime)
                    html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/bookingset.html', {'company':company,'staff':staff,'service':service, 'date':date, 'time':time, 'month':month, 'year':year, 'day':day }, request)
            
            else:
                html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/bookingerror.html', {'company':company,'staff':staff,'service':service, 'date':date, 'time':time, 'month':month, 'year':year, 'day':day }, request)
            lock.release()
        return JsonResponse({'form_is_invalid':False, 'html_content': html_content})
         
class renderLoginPage(View):
    def get(self, request):
        company = request.viewing_company
        account_form = AccountAuthenticationForm()
        company=request.viewing_company
        s_id = request.session.get('service_id')
        staff_id = request.session.get('staff_id')
        month = request.session.get('month')
        year = request.session.get('year')
        day = request.session.get('day')
        time = request.session.get('time')
        staff = get_object_or_404(StaffMember, id=staff_id)
        service = get_object_or_404(Services, id=s_id)
        date = datetime.date(year, month, day)
        html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/login/bookmeuser.html', {'account_form':account_form, 'company':company, 'staff':staff,'service':service, 'date':date, 'time':time }, request)
        return JsonResponse({'html_content': html_content})

    def post(self, request):
        company = request.viewing_company

        s_id = request.session.get('service_id')
        staff_id = request.session.get('staff_id')
        month = request.session.get('month')
        year = request.session.get('year')
        day = request.session.get('day')
        time = request.session.get('time')
        make = request.session.get('vehmake')
        model = request.session.get('vehmodel')
        vehyear = request.session.get('vehyear')
        trim = request.session.get('vehtrim')
        bookinglist = request.session.get('formlist')


        # s_id = int(request.POST.get('service_id'))
        # staff_id = int(request.POST.get('staff_id'))
        # time = request.POST.get('time')
        # month = int(request.POST.get('month'))
        # year = int(request.POST.get('year'))
        # day = int(request.POST.get('day'))
        date = datetime.date(year, month, day)
        staff = StaffMember.objects.get(pk=staff_id)
        service = Services.objects.get(pk=s_id)
        # make = request.POST.get('make')
        # model = request.POST.get('model')
        # vehyear = request.POST.get('vehyear')
        # trim = request.POST.get('trim')

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        
        if user == None:
            return JsonResponse({'notvalid':True})
        else:
            if user.is_active:
                login(request, user)
            else:
                return JsonResponse({'notvalid':True})

        price = service.price
        startdate = datetime.datetime(year,month,day)
        starttime = datetime.datetime.strptime(time,'%I:%M %p').time()
        start = datetime.datetime.combine(startdate, starttime)
        end = start + datetime.timedelta(hours=service.duration_hour,minutes=service.duration_minute)
        start = timezone.localtime(timezone.make_aware(start))
        end = timezone.localtime(timezone.make_aware(end))
        
        #Validate the issues first
        if company.returning:
            if company.clients.filter(user=user, first_name=user.first_name).exists():
                pass
            #Check if the client object was already created by the company
            elif company.clients.filter(phone=user.phone, first_name=user.first_name).exists():
                pass
            elif company.clients.filter(email=user.email, first_name=user.first_name).exists():
                pass
            else:
                return JsonResponse({'notonclientlist':True})
        lock = multiprocessing.Lock()
        lock.acquire()
        bcount = Bookings.objects.filter(company=company, staffmem=staff, start__gte=start, end__lte=end, is_cancelled_user=False,is_cancelled_company=False, is_cancelled_request=False).count()
        if bcount<1:
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
            booking = Bookings.objects.create(user=user,guest=guest,service=service, staffmem=staff, company=company,start=start, end=end, price=price)
            booking.save()
            if company.category.name == 'Automotive Services':
                bookinform1 = bookingForm.objects.create(booking=booking, label='Vehicle Year', text=vehyear.replace('%20',' '))
                bookinform2 = bookingForm.objects.create(booking=booking, label='Vehicle Make', text=make.replace('%20',' '))
                bookinform3 = bookingForm.objects.create(booking=booking, label='Vehicle Model', text=model.replace('%20',' '))
                bookinform4 = bookingForm.objects.create(booking=booking, label='Vehicle Trim', text=trim.replace('%20',' '))
                bookinform1.save()
                bookinform2.save()
                bookinform3.save()
                bookinform4.save()
            
            for newformfield in bookinglist:
                # fieldname = request.POST.get(str(newformfield.id))
                bookinform = bookingForm.objects.create(booking=booking, label=newformfield[1], text=newformfield[0])
                bookinform.save()
            if service.request:
                reqc = CompanyReq.objects.create(guest=guest, company=company, is_addbooking=True)
                booking.bookingreq = reqc
                booking.save()
                #Send request sent and recieved to customer and client respectively
                #Email
                emailRequestServiceClient.delay(booking.id)
                emailRequestServiceCompany.delay(booking.id)
                #Text
                if company.subscriptionplan >= 1:
                    send_sms_requestService_company.delay(booking.id)
                    send_sms_requestService_client.delay(booking.id)
                html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/requestServiceSent.html', {'company':company,'staff':staff,'booking':booking }, request)
            else:
                #Send conf and reminder emails
                confirmedEmail.delay(booking.id)
                confirmedEmailCompany.delay(booking.id)
                confirmtime = 30
                if service.checkintime:
                    confirmtime = service.checkintime + 30
                startTime = timezone.localtime(start - datetime.timedelta(minutes=confirmtime))
                reminderEmail.apply_async(args=[booking.id], eta=startTime, task_id=booking.slug)
                # Confirm the appointment through texts with the client
                if company.subscriptionplan >= 1:
                    send_sms_confirmed_client.delay(booking.id)
                    send_sms_reminder_client.apply_async(args=[booking.id], eta=startTime)
                html_content = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/bookingset.html', {'company':company,'staff':staff,'service':service, 'date':date, 'time':time, 'month':month, 'year':year, 'day':day }, request)
        lock.release()
        return JsonResponse({'notvalid':False, 'html_content':html_content})

class loginReturningCustomer(View):
    def post(self, request):
        company = request.viewing_company
        # s_id = int(request.POST.get('service_id'))
        s_id = request.session.get('service_id')

        service = Services.objects.get(pk=s_id)

        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        request.session['service_id'] = s_id



        if user == None:
            return JsonResponse({'notvalid':True, 'errormsg':'Email and password combination is not correct. Please try again.'})
        else:
            if user.is_active:
                login(request, user)
                staff = company.staffmembers.filter(services=service)
                if company.clients.filter(user=user, first_name=user.first_name).exists():
                    html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/services_offered_staff.html', {'company':company,'staff':staff, 'service':service}, request)
                    return JsonResponse({'html_content':html, 'loggedinuser':False})

                #Check if the client object was already created by the company
                elif company.clients.filter(phone=user.phone, first_name=user.first_name).exists():
                    html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/services_offered_staff.html', {'company':company,'staff':staff, 'service':service}, request)
                    return JsonResponse({'html_content':html, 'loggedinuser':False})

                elif company.clients.filter(email=user.email, first_name=user.first_name).exists():
                    html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/services_offered_staff.html', {'company':company,'staff':staff, 'service':service}, request)
                    return JsonResponse({'html_content':html, 'loggedinuser':False})
                else:
                    html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/bookingRequest.html', {'company':company,'service':service}, request)
                    return JsonResponse({'html_content':html, 'loggedinuser':True})
            else:
                return JsonResponse({'notvalid':True, 'errormsg':'Your account has been deactivated for some time. Please contact support@bookme.to'})


class requestSpot(View):
    def post(self, request):
        # s_id = int(request.POST.get('service_id'))
        s_id = request.session.get('service_id')
        service = Services.objects.get(pk=s_id)
        if request.user.is_authenticated:
            user = get_object_or_404(Account, email=request.user.email)
        else:
            account_form = AccountAuthenticationForm()
            html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/login/returnClient.html', {'account_form':account_form, 'company':company, 'service':service}, request)
            return JsonResponse({'html_content':html})
        company = request.viewing_company
        requestUser = CompanyReq.objects.filter(user=user, company=company).exists()
        if not requestUser:
            requestUser = CompanyReq.objects.create(user=user, company=company, is_addusertolist=True)
            requestUser.save()
            requestToBeClient.delay(requestUser.id)
        html = render_to_string('bookingpage/multiplestaff/bookingpage/partials/confirmationside/requestSent.html', {'company':company, 'service':service}, request)
        return JsonResponse({'html_content':html, 'returning':True})