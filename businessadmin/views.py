from django.shortcuts import render, get_object_or_404, redirect
from .forms import BusinessRegistrationForm, AddHoursForm, UpdateCompanyForm, AddClientForm, AddNotesForm, CreateSmallBizForm, AddBookingForm
from django.contrib.auth.decorators import login_required
from business.models import Company, SubCategory, OpeningHours, Services, Gallary, Amenities, Clients, CompanyReq
from account.models import Account
from account.forms import UpdatePersonalForm
from account.tasks import bizCreatedEmailSent, consumerCreatedEmailSent
from consumer.models import Bookings, Reviews
from account.forms import AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django_hosts.resolvers import reverse
from django.http import JsonResponse
import json
from business.forms import AddCompanyForm, AddServiceForm, UpdateServiceForm, BookingSettingForm
from django.forms import inlineformset_factory
from django.views import View
from slugify import slugify
from .forms import MainPhoto
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from businessadmin.tasks import addedOnCompanyList, requestToBeClient, appointmentCancelled
from account.tasks import reminderEmail, confirmedEmail, consumerCreatedEmailSent
# Create your views here.
def businessadmin(request):
    user = request.user

    return render(request, 'welcome/welcome.html', {'user':user, 'none':'d-none'})

def pricingViews(request):
    user = request.user
    return render(request, 'welcome/pricing.html', {'user':user,'none':'d-none'})

def faqBusinessViews(request):
    user = request.user
    return render(request, 'welcome/faq.html', {'user':user,'none':'d-none'})

def createNewBusiness(request):
    user = request.user
    user_form = CreateSmallBizForm()
    if not user.is_authenticated:
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})

    if request.method == 'POST':
        user_form = CreateSmallBizForm(request.POST)
        
        if user_form.is_valid():
            email = user_form.cleaned_data.get('email')
            phone = user_form.cleaned_data.get('phone')
            bname = user_form.cleaned_data.get('business_name')
            company = Company.objects.create(user=user,business_name=bname,email=email,phone=phone,
                                                description='',address='',postal='',
                                                state='',city='',status='draft')
            company.save()
            biz_hours = OpeningHours.objects.bulk_create([
                OpeningHours(company=company, weekday=0,is_closed=True),
                OpeningHours(company=company, weekday=1,is_closed=False),
                OpeningHours(company=company, weekday=2,is_closed=False),
                OpeningHours(company=company, weekday=3,is_closed=False),
                OpeningHours(company=company, weekday=4,is_closed=False),
                OpeningHours(company=company, weekday=5,is_closed=False),
                OpeningHours(company=company, weekday=6,is_closed=True),
            ])
            user.is_business=True
            user.save()
            return redirect(reverse('completeprofile', host='bizadmin'))
        else:
            context['business_registration_form'] = user_form

    if user.on_board:
        return redirect(reverse('home', host='bizadmin'))
    
    
    return render(request, 'account/createbusiness.html', {'user':user, 'none':'d-none', 'user_form':user_form})

def completeViews(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    biz_form = AddCompanyForm()
    service_form = AddServiceForm()
    company = Company.objects.get(user=user)
    sunday = OpeningHours.objects.get(company=company, weekday=0)
    monday = OpeningHours.objects.get(company=company, weekday=1)
    tuesday = OpeningHours.objects.get(company=company, weekday=2)
    wednesday = OpeningHours.objects.get(company=company, weekday=3)
    thursday = OpeningHours.objects.get(company=company, weekday=4)
    friday = OpeningHours.objects.get(company=company, weekday=5)
    saturday = OpeningHours.objects.get(company=company, weekday=6)
    booking_form = BookingSettingForm()
    sundayform = AddHoursForm(initial={'dayfrom':sunday.from_hour, 'dayto':sunday.to_hour}, prefix='sun')
    mondayform = AddHoursForm(initial={'dayfrom':monday.from_hour, 'dayto':monday.to_hour},prefix='mon')
    tuesdayform = AddHoursForm(initial={'dayfrom':tuesday.from_hour, 'dayto':tuesday.to_hour},prefix='tues')
    wednesdayform = AddHoursForm(initial={'dayfrom':wednesday.from_hour, 'dayto':wednesday.to_hour},prefix='wed')
    thursdayform = AddHoursForm(initial={'dayfrom':thursday.from_hour, 'dayto':thursday.to_hour},prefix='thurs')
    fridayform = AddHoursForm(initial={'dayfrom':friday.from_hour, 'dayto':friday.to_hour},prefix='fri')
    saturdayform = AddHoursForm(initial={'dayfrom':saturday.from_hour, 'dayto':saturday.to_hour},prefix='sat')
    if user.on_board:
        return redirect(reverse('home', host='bizadmin')) 
    if request.method == 'POST':
        biz_form = AddCompanyForm(request.POST)
        booking_form = BookingSettingForm(request.POST)
        sundayform = AddHoursForm(request.POST,prefix='sun')
        mondayform = AddHoursForm(request.POST,prefix='mon')
        tuesdayform = AddHoursForm(request.POST,prefix='tues')
        wednesdayform = AddHoursForm(request.POST, prefix='wed')
        thursdayform = AddHoursForm(request.POST,prefix='thurs')
        fridayform = AddHoursForm(request.POST,prefix='fri')
        saturdayform = AddHoursForm(request.POST,prefix='sat')
        if biz_form.is_valid() and booking_form.is_valid():
            category = biz_form.cleaned_data.get('category')
            subcategory = biz_form.cleaned_data.get('subcategory')
            description = biz_form.cleaned_data.get('description')
            address = biz_form.cleaned_data.get('address')
            postal = biz_form.cleaned_data.get('postal')
            state = biz_form.cleaned_data.get('state')
            city = biz_form.cleaned_data.get('city')
            interval = booking_form.cleaned_data.get('interval')
            notes = booking_form.cleaned_data.get('notes')
            cancellation = booking_form.cleaned_data.get('cancellation')
            subdomain = request.POST.get('subdomain', company.slug)
            returning = request.POST.get('returning', False)
            sun_from = request.POST.get('sun-dayfrom')
            sun_to = request.POST.get('sun-dayto')
            sun_closed = not request.POST.get('sunOpen', False)
            mon_from = request.POST.get('mon-dayfrom')
            mon_to = request.POST.get('mon-dayto')
            mon_closed = not request.POST.get('monOpen', False)
            tues_from = request.POST.get('tues-dayfrom')
            tues_to = request.POST.get('tues-dayto')
            tues_closed = not request.POST.get('tuesOpen', False)
            wed_from = request.POST.get('wed-dayfrom')
            wed_to = request.POST.get('wed-dayto')
            wed_closed = not request.POST.get('wedOpen', False)
            thurs_from = request.POST.get('thurs-dayfrom')
            thurs_to = request.POST.get('thurs-dayto')
            thurs_closed = not request.POST.get('thursOpen', False)
            fri_from = request.POST.get('fri-dayfrom')
            fri_to = request.POST.get('fri-dayto')
            fri_closed = not request.POST.get('friOpen', False)
            sat_from = request.POST.get('sat-dayfrom')
            sat_to = request.POST.get('sat-dayto')
            sat_closed = not request.POST.get('satOpen', False)

            status = 'published'
            company.category = category
            company.description = description
            company.address = address
            company.postal = postal
            company.state = state
            company.city = city
            company.status = status
            company.interval = interval
            if returning:
                company.returning = True
            company.notes = notes
            company.cancellation = cancellation
            if subdomain != company.slug:
                if not Company.objects.filter(slug=subdomain).exists():
                    company.slug = slugify(subdomain)
            company.save()
            user.on_board = True
            user.save()
            objs = [
                OpeningHours.objects.get(company=company, weekday=0),
                OpeningHours.objects.get(company=company, weekday=1),
                OpeningHours.objects.get(company=company, weekday=2),
                OpeningHours.objects.get(company=company, weekday=3),
                OpeningHours.objects.get(company=company, weekday=4),
                OpeningHours.objects.get(company=company, weekday=5),
                OpeningHours.objects.get(company=company, weekday=6),
            ]
            objs[0].is_closed = sun_closed
            objs[1].is_closed = mon_closed
            objs[2].is_closed = tues_closed
            objs[3].is_closed = wed_closed
            objs[4].is_closed = thurs_closed
            objs[5].is_closed = fri_closed
            objs[6].is_closed = sat_closed

            objs[0].from_hour = datetime.strptime(sun_from,"%I:%M %p")
            objs[1].from_hour = datetime.strptime(mon_from,"%I:%M %p")
            objs[2].from_hour = datetime.strptime(tues_from,"%I:%M %p")
            objs[3].from_hour = datetime.strptime(wed_from,"%I:%M %p")
            objs[4].from_hour = datetime.strptime(thurs_from,"%I:%M %p")
            objs[5].from_hour = datetime.strptime(fri_from,"%I:%M %p")
            objs[6].from_hour = datetime.strptime(sat_from,"%I:%M %p")

            objs[0].to_hour = datetime.strptime(sun_to,"%I:%M %p")
            objs[1].to_hour = datetime.strptime(mon_to,"%I:%M %p")
            objs[2].to_hour = datetime.strptime(tues_to,"%I:%M %p")
            objs[3].to_hour = datetime.strptime(wed_to,"%I:%M %p")
            objs[4].to_hour = datetime.strptime(thurs_to,"%I:%M %p")
            objs[5].to_hour = datetime.strptime(fri_to,"%I:%M %p")
            objs[6].to_hour = datetime.strptime(sat_to,"%I:%M %p")

            OpeningHours.objects.bulk_update(objs,['is_closed','from_hour','to_hour'])
            for s in subcategory:
                company.subcategory.add(s)
            bizCreatedEmailSent.delay(user.id)
            return redirect(reverse('home', host='bizadmin'))
        
        # else:
        #     print(sundayform.errors)

    subcategories = SubCategory.objects.all()
    company = Company.objects.get(user=user)
    services = Services.objects.filter(business=company)
    

    return render(request, 'bizadmin/dashboard/profile/addcompany.html', {'sundayform':sundayform,'saturdayform':saturdayform,'mondayform':mondayform,'tuesdayform':tuesdayform,'wednesdayform':wednesdayform,'thursdayform':thursdayform,'fridayform':fridayform,
                                                                                'booking_form':booking_form,'biz_form':biz_form, 'service_form':service_form,'subcategories':subcategories,'company':company,
                                                                                'services':services})

def load_subcat(request):
    cat_id = request.GET.get('category')
    if cat_id:
        subcategories = SubCategory.objects.filter(category_id=cat_id).order_by('name')
    else:
        subcategories = None
    return render(request, 'bizadmin/dashboard/profile/addcompanyhelper/subcat_dropdown_list_options.html', {'subcategories': subcategories})

class subdomainCheck(View):
    def post(self, request):
        data=json.loads(request.body)
        subdomain = data['subdomain']
        company = Company.objects.get(user=request.user)
        if not subdomain:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        if (company.slug!=str(subdomain)) and (Company.objects.filter(slug=subdomain).exists()):
            return JsonResponse({'email_error':'This subdomain already exists! Please try another.','email_valid':True})

        if subdomain != slugify(subdomain):
            return JsonResponse({'email_error':'Subdomains must only contain lowercase letters, numbers and hyphens.','email_valid':True})
        return JsonResponse({'email_valid':False})

def signupViews(request):
    context = {}
    if request.method == 'POST':
        user_form = BusinessRegistrationForm(request.POST)
        
        if user_form.is_valid():
            user_form.save()
            email = user_form.cleaned_data.get('email')
            raw_pass = user_form.cleaned_data.get('password1')
            phone = user_form.cleaned_data.get('phone')
            bname = request.POST.get('bname', '')
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            company = Company.objects.create(user=account,business_name=bname,email=email,phone=phone,
                                                description='',address='',postal='',
                                                state='',city='',status='draft')
            company.save()
            biz_hours = OpeningHours.objects.bulk_create([
                OpeningHours(company=company, weekday=0,is_closed=True),
                OpeningHours(company=company, weekday=1,is_closed=False),
                OpeningHours(company=company, weekday=2,is_closed=False),
                OpeningHours(company=company, weekday=3,is_closed=False),
                OpeningHours(company=company, weekday=4,is_closed=False),
                OpeningHours(company=company, weekday=5,is_closed=False),
                OpeningHours(company=company, weekday=6,is_closed=True),
            ])
            return redirect(reverse('completeprofile', host='bizadmin'))
        else:
            context['business_registration_form'] = user_form
            
    else:
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
    return render(request, 'account/bussignup.html', {'user_form':user_form, 'none':'d-none'})

def loginViews(request):
    context = {}
    if request.method == 'POST':
        user_form = AccountAuthenticationForm(request.POST)
        if user_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            account = authenticate(email=email, password=password)
            if account:
                login(request, account)
                if account.is_business:
                    if account.on_board:
                        return redirect(reverse('home', host='bizadmin'))
                    else:
                        return redirect(reverse('completeprofile', host='bizadmin'))
                        
                else:
                    return redirect(reverse('newbizcreate', host='bizadmin'))
        else:
            context['business_registration_form'] = user_form
            
    else:
        user_form = AccountAuthenticationForm()
        context['business_registration_form'] = user_form
    return render(request, 'account/buslogin.html', {'user_form':user_form, 'none':'d-none'})

def profileViews(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            image_form = MainPhoto()
            personal_data = {'first_name': user.first_name, 
                    'last_name': user.last_name, 
                    'email':user.email, 
                    'phone':user.phone}
            personal_form = UpdatePersonalForm(initial=personal_data)
            return render(request, 'bizadmin/dashboard/account/profile.html',{'company':company, 'image_form':image_form, 'personal_form':personal_form})
        else:
            return redirect(reverse('completeprofile', host='bizadmin'))
    else:
        loginViews(request)
    
class personDetailSave(View):
    def post(self, request):
        personal_form = UpdatePersonalForm(request.POST, instance=request.user)
        acct = get_object_or_404(Account, email=request.user)
        if personal_form.is_valid():
            acct.first_name = personal_form.cleaned_data.get('first_name')
            acct.last_name = personal_form.cleaned_data.get('last_name')
            acct.email = personal_form.cleaned_data.get('email')
            acct.phone = personal_form.cleaned_data.get('phone')
            acct.save()
            return JsonResponse({'good':"The data was good"})
        else:
            return JsonResponse({'errors':'There were errors'})

def profileBillingViews(request):
    return render(request,'bizadmin/dashboard/account/billing.html')

@login_required()
def profileSecurityViews(request):
    company = get_object_or_404(Company, user=request.user)
    return render(request,'bizadmin/dashboard/account/security.html', {'company':company})

@login_required()
def notifViews(request):
    company = get_object_or_404(Company, user=request.user)
    notesForm = AddNotesForm(initial={'notes':company.notes})
    return render(request,'bizadmin/dashboard/account/notification.html', {'company':company, 'notesForm':notesForm})

class updateEmailSetting(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['emailReminder']
        company = get_object_or_404(Company, user=request.user)
        if email == True:
            company.emailReminders = True
        else:
            company.emailReminders = False
        company.save()

        return JsonResponse({'good':'girl'})

class notesUpdate(View):
    def post(self, request):
        data = json.loads(request.body)
        notesShow = data['isnotes']
        company  = get_object_or_404(Company, user=request.user)
        notes = data['notes']
        company.notes = notes
        # print(notes)
        if notesShow:
            company.shownotes = True
        else:
            company.shownotes = False
        company.save()

        return JsonResponse({'good':'success'})


@login_required
def scheduleView(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            day = datetime.today().weekday() + 1
            if day >= 7:
                day = 0
            openhour = OpeningHours.objects.get(company=company, weekday=day).from_hour
            bookings = Bookings.objects.filter(company=company, is_cancelled_user=False, is_cancelled_company=False)
            addbooking = AddBookingForm(initial={'company':company, 'timepick':openhour, 'datepick':datetime.today().strftime('%m/%d/%Y')})
            return render(request, 'bizadmin/dashboard/schedule.html', {'company':company, 'bookings':bookings, 'addbooking':addbooking})
        else:
            return redirect(reverse('completeprofile', host='bizadmin'))
    else:
        loginViews(request)

def fileUploadView(request):
    if request.POST:
        return JsonResponse({'works':'works'})

def LogoutView(request):
    logout(request)
    return render(request, 'welcome/welcome.html', {'business':False})

from django.template.loader import render_to_string
def save_service_form(request, form, template_name):
    data=dict()
    if request.method=='POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            price_type = form.cleaned_data.get('price_type')
            price = form.cleaned_data.get('price')
            duration_hour = form.cleaned_data.get('duration_hour')
            duration_minute = form.cleaned_data.get('duration_minute')
            checkintime=form.cleaned_data.get('checkintime')
            padding=form.cleaned_data.get('padding')
            paddingtime_hour=form.cleaned_data.get('paddingtime_hour')
            paddingtime_minute=form.cleaned_data.get('paddingtime_minute')
            avail = True
            company = Company.objects.get(user=request.user)
            service = Services.objects.create(business=company,name=name,description=description,price=price, available=avail, 
                                                price_type=price_type,duration_hour=duration_hour,duration_minute=duration_minute,checkintime=checkintime,
                                                padding=padding,paddingtime_hour=paddingtime_hour,paddingtime_minute=paddingtime_minute)
            service.save()
            data['form_is_valid'] = True
            services = Services.objects.filter(business=company)
            data['html_service_list'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_list.html', {'services':services})
            data['view'] = 'Your service has been created!'
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
    
    context = {'service_form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

#used in the onboarding page
def createserviceViews(request):
    if request.method=='POST':
        service_form = AddServiceForm(request.POST)
    else:
        service_form = AddServiceForm()
    return save_service_form(request, service_form, 'bizadmin/dashboard/profile/services/partial_service_create.html')

#used in the bizadmin page
class createserviceAPI(View):
    def post(self,request):
        form = AddServiceForm(request.POST)
        data = dict()
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_type = form.cleaned_data.get('price_type')
            price = form.cleaned_data.get('price')
            duration_hour = form.cleaned_data.get('duration_hour')
            duration_minute = form.cleaned_data.get('duration_minute')
            checkintime=form.cleaned_data.get('checkintime')
            padding=form.cleaned_data.get('padding')
            paddingtime_hour=form.cleaned_data.get('paddingtime_hour')
            paddingtime_minute=form.cleaned_data.get('paddingtime_minute')
            avail = True
            company = Company.objects.get(user=request.user)
            service = Services.objects.create(business=company,name=name,description=description,price=price, available=avail, 
                                                price_type=price_type,duration_hour=duration_hour,duration_minute=duration_minute,checkintime=checkintime,
                                                padding=padding,paddingtime_hour=paddingtime_hour,paddingtime_minute=paddingtime_minute)
            service.save()
            data['form_is_valid'] = True
            data['view'] = 'Your service has been created!'
            data['icon'] = 'success'
        else:
            data['form_is_valid'] = False
            data['view'] = 'Your service was not created. There was an error.'
            data['icon'] = 'error'
        company = Company.objects.get(user=request.user)
        services = Services.objects.filter(business=company)
        paginator = Paginator(services, 5)
        page = request.GET.get('page')
        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)
        data['html_service_list'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_list.html', {'page':page,'services':services})
        return JsonResponse(data)

class createclientAPI(View):
    def post(self,request):
        form = AddClientForm(request.POST)
        data = dict()
        if form.is_valid():
            company = Company.objects.get(user=request.user)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            address = form.cleaned_data.get('address')
            postal = form.cleaned_data.get('postal')
            city = form.cleaned_data.get('city')
            province = form.cleaned_data.get('province')
            user = None
            if email:
                if Account.objects.filter(email = email).exists():
                    user = Account.objects.get(email=email)
            elif phone:
                if Account.objects.filter(phone=phone).exists():
                    user = Account.objects.filter(phone=phone).first()
            
            Clients.objects.create(user=user, company=company, first_name=first_name, last_name=last_name, email=email,phone=phone,
                                city=city,postal=postal,province=province,address=address)
            clients = company.clients.all()
            data['form_is_valid'] = True
            data['view'] = 'Your client has been added!'
            data['icon'] = 'success'
        else:
            data['form_is_valid'] = False
            data['view'] = 'Your client was not added. There was an error.'
            data['icon'] = 'error'
        data['html_service_list'] = render_to_string('bizadmin/companydetail/client/partial/partial_client_list.html', {'clients':clients})
        return JsonResponse(data)

class deleteclientAPI(View):
    def get(self, request, pk):
        data = dict()
        company = Company.objects.get(user=request.user)
        client = get_object_or_404(Clients, pk=pk, company=company)
        client.delete()
        clients = company.clients.all()
        data['html_service_list'] = render_to_string('bizadmin/companydetail/client/partial/partial_client_list.html', {'clients':clients})
        return JsonResponse(data)



#used in the onboarding page
def deleteserviceViews(request, pk):

    company = Company.objects.get(user=request.user)
    service = get_object_or_404(Services, pk=pk, business=company)
    data = dict()
    if request.method=='POST':
        service.delete()
        data['form_is_valid']=True
        services = Services.objects.filter(business=company)
        data['html_service_list'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_list.html', {'services':services})
        data['view'] = 'Your service has been deleted'
    else:
        context = {'service':service}
        data['html_form'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_delete.html', context, request=request)
    return JsonResponse(data)

#used in the bizadmin page
class deleteserviceAPI(View):
    def get(self, request, pk):
        data = dict()
        company = Company.objects.get(user=request.user)
        service = get_object_or_404(Services, pk=pk, business=company)
        service.delete()
        services = Services.objects.filter(business=company)
        paginator = Paginator(services, 5)
        page = request.GET.get('page')
        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)
        data['html_service_list'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_list.html', {'page':page,'services':services})
        return JsonResponse(data)

class updateclientAPI(View):
    def get(self, request, pk):
        company = Company.objects.get(user=request.user)
        client = get_object_or_404(Clients, pk=pk,  company=company)
        dat = {'first_name': client.first_name, 'last_name': client.last_name, 'email': client.email,  'phone': client.phone,  'address': client.address,  'province':client.province, 'postal':client.postal, 'city':client.city}
        data=dict()
        form = AddClientForm(initial=dat)
        context = {'form':form, 'client':client}
        data['html_form'] = render_to_string('bizadmin/companydetail/client/partial/partial_client_update.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, pk):
        company = Company.objects.get(user=request.user)
        client = get_object_or_404(Clients, pk=pk, company=company)
        form = AddClientForm(request.POST)
        data=dict()
        if form.is_valid():
            client.first_name = form.cleaned_data.get('first_name')
            client.last_name = form.cleaned_data.get('last_name')
            client.email = form.cleaned_data.get('email')
            client.phone = form.cleaned_data.get('phone')
            client.address = form.cleaned_data.get('address')
            client.province = form.cleaned_data.get('province')
            client.postal = form.cleaned_data.get('postal')
            client.city = form.cleaned_data.get('city')
            client.save()
            data['form_is_valid'] = True
            clients = company.clients.all()
            data['html_service_list'] = render_to_string('bizadmin/companydetail/client/partial/partial_client_list.html', {'clients':clients})
            data['view'] = 'The clients information has been updated'
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)


class saveBusinessHours(View):
    def post(self, request):
        sun_from = request.POST['sunOpenHour']
        sun_to = request.POST['sunCloseHour']
        sun_closed = not request.POST.get('sunOpen', False)
        mon_from = request.POST['monOpenHour']
        mon_to = request.POST['monCloseHour']
        mon_closed = not request.POST.get('monOpen', False)
        tues_from = request.POST['tuesOpenHour']
        tues_to = request.POST['tuesCloseHour']
        tues_closed = not request.POST.get('tuesOpen', False)
        wed_from = request.POST['wedOpenHour']
        wed_to = request.POST['wedCloseHour']
        wed_closed = not request.POST.get('wedOpen', False)
        thurs_from = request.POST['thursOpenHour']
        thurs_to = request.POST['thursCloseHour']
        thurs_closed = not request.POST.get('thursOpen', False)
        fri_from = request.POST['friOpenHour']
        fri_to = request.POST['friCloseHour']
        fri_closed = not request.POST.get('friOpen', False)
        sat_from = request.POST['satOpenHour']
        sat_to = request.POST['satCloseHour']
        sat_closed = not request.POST.get('satOpen', False)
        company = Company.objects.get(user=request.user)
        objs = [
            OpeningHours.objects.get(company=company, weekday=0),
            OpeningHours.objects.get(company=company, weekday=1),
            OpeningHours.objects.get(company=company, weekday=2),
            OpeningHours.objects.get(company=company, weekday=3),
            OpeningHours.objects.get(company=company, weekday=4),
            OpeningHours.objects.get(company=company, weekday=5),
            OpeningHours.objects.get(company=company, weekday=6),
        ]
        objs[0].is_closed = sun_closed
        objs[1].is_closed = mon_closed
        objs[2].is_closed = tues_closed
        objs[3].is_closed = wed_closed
        objs[4].is_closed = thurs_closed
        objs[5].is_closed = fri_closed
        objs[6].is_closed = sat_closed

        objs[0].from_hour = datetime.strptime(sun_from,"%I:%M %p")
        objs[1].from_hour = datetime.strptime(mon_from,"%I:%M %p")
        objs[2].from_hour = datetime.strptime(tues_from,"%I:%M %p")
        objs[3].from_hour = datetime.strptime(wed_from,"%I:%M %p")
        objs[4].from_hour = datetime.strptime(thurs_from,"%I:%M %p")
        objs[5].from_hour = datetime.strptime(fri_from,"%I:%M %p")
        objs[6].from_hour = datetime.strptime(sat_from,"%I:%M %p")

        objs[0].to_hour = datetime.strptime(sun_to,"%I:%M %p")
        objs[1].to_hour = datetime.strptime(mon_to,"%I:%M %p")
        objs[2].to_hour = datetime.strptime(tues_to,"%I:%M %p")
        objs[3].to_hour = datetime.strptime(wed_to,"%I:%M %p")
        objs[4].to_hour = datetime.strptime(thurs_to,"%I:%M %p")
        objs[5].to_hour = datetime.strptime(fri_to,"%I:%M %p")
        objs[6].to_hour = datetime.strptime(sat_to,"%I:%M %p")
        OpeningHours.objects.bulk_update(objs,['is_closed','from_hour','to_hour'])
        data = {'good':True}
        return JsonResponse(data)

#used in the onboarding page
def updateserviceViews(request, pk):
    service = get_object_or_404(Services, pk=pk)
    company = Company.objects.get(user=request.user)
    dat = {'name': service.name, 'description': service.description, 'price_type':service.price_type, 'price':service.price, 'available':service.available, 'duration_hour':service.duration_hour, 'duration_minute':service.duration_minute, 'checkintime':service.checkintime, 'padding':service.padding, 'paddingtime_hour':service.paddingtime_hour, 'paddingtime_minute':service.paddingtime_minute}
    data=dict()
    if request.method=='POST':
        form = UpdateServiceForm(request.POST)
        if form.is_valid():
            
            service.name = form.cleaned_data.get('name')
            service.description = form.cleaned_data.get('description')
            service.price_type = form.cleaned_data.get('price_type')
            service.price = form.cleaned_data.get('price')
            service.duration_hour = form.cleaned_data.get('duration_hour')
            service.duration_minute = form.cleaned_data.get('duration_minute')
            service.checkintime = form.cleaned_data.get('checkintime')
            service.padding = form.cleaned_data.get('padding')
            service.paddingtime_hour = form.cleaned_data.get('paddingtime_hour')
            service.paddingtime_minute = form.cleaned_data.get('paddingtime_minute')
            service.avail = True
            company = Company.objects.get(user=request.user)
            service.save()
            data['form_is_valid'] = True
            services = Services.objects.filter(business=company)
            paginator = Paginator(services, 5)
            page = request.GET.get('page')
            try:
                services = paginator.page(page)
            except PageNotAnInteger:
                services = paginator.page(1)
            except EmptyPage:
                services = paginator.page(paginator.num_pages)
            data['html_service_list'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_list.html', {'page':page,'services':services})
            data['html_service_list_bizadmin'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_list.html', {'page':page,'services':services})
            data['view'] = 'Your service has been updated'
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
    else:
        form = UpdateServiceForm(initial=dat)
    context = {'service_form':form, 'service':service}
    data['html_form'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_update.html', context, request=request)
    return JsonResponse(data)

#Used in the bizadmin page
class updateserviceAPI(View):
    def get(self, request, pk):
        service = get_object_or_404(Services, pk=pk)
        company = Company.objects.get(user=request.user)
        dat = {'name': service.name, 'description': service.description, 'price_type':service.price_type, 'price':service.price, 'available':service.available, 'duration_hour':service.duration_hour, 'duration_minute':service.duration_minute, 'checkintime':service.checkintime, 'padding':service.padding, 'paddingtime_hour':service.paddingtime_hour, 'paddingtime_minute':service.paddingtime_minute}
        data=dict()
        form = UpdateServiceForm(initial=dat)
        
        context = {'service_form':form,'service':service}
        data['html_form'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_update.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, pk):
        service = get_object_or_404(Services, pk=pk)
        company = Company.objects.get(user=request.user)
        form = UpdateServiceForm(request.POST)
        data=dict()
        if form.is_valid():
            service.name = form.cleaned_data.get('name')
            service.description = form.cleaned_data.get('description')
            service.price_type = form.cleaned_data.get('price_type')
            service.price = form.cleaned_data.get('price')
            service.duration_hour = form.cleaned_data.get('duration_hour')
            service.duration_minute = form.cleaned_data.get('duration_minute')
            service.checkintime = form.cleaned_data.get('checkintime')
            service.padding = form.cleaned_data.get('padding')
            service.paddingtime_hour = form.cleaned_data.get('paddingtime_hour')
            service.paddingtime_minute = form.cleaned_data.get('paddingtime_minute')
            service.avail = True
            company = Company.objects.get(user=request.user)
            service.save()
            data['form_is_valid'] = True
            services = Services.objects.filter(business=company)
            paginator = Paginator(services, 5)
            page = request.GET.get('page')
            try:
                services = paginator.page(page)
            except PageNotAnInteger:
                services = paginator.page(1)
            except EmptyPage:
                services = paginator.page(paginator.num_pages)
            data['html_service_list'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_list.html', {'page':page,'services':services})
            data['view'] = 'Your service has been updated'
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)



## Adding the homepage views and all stuff required for the homepage
from django.utils import timezone
import pytz
from datetime import timedelta, datetime
from django.db.models import Sum
from decimal import Decimal
from taggit.models import Tag
@login_required
def homepageViews(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            #Percentage for business page photos
            bpp = 0
            #Client added to the database percentage
            cdb = 0
            #Services added to the database percentage
            sdb = 0
            #Tags add to the database
            tpp = 0

            #Total Basic Account Setup
            if company.tags.all(): 
                tpp = 100
            
            if company.image:
                bpp = bpp + 25
            gallary = Gallary.objects.filter(company=company)
            if gallary:
                count = gallary.count()
                if count==1:
                    bpp = bpp +25
                elif count == 2:
                    bpp = bpp +50
                else:
                    bpp =100
            if company.clients:
                cdb = 100
            
            services = Services.objects.filter(business=company)

            for service in services:
                sdb = sdb + 25
                if sdb >= 100:
                    sdb = 100
                    break
            
            ttpp = int((bpp/4) + (cdb/4)+ (sdb/4) + (tpp/4))

            week = timezone.now() - timedelta(days=7)
            twoweek = week - timedelta(days=7)
            threeweek = twoweek - timedelta(days=7)
            fourweek = threeweek - timedelta(days=7)
            week1 = Bookings.objects.filter(company=company, end__gte=week, end__lte=timezone.now()).aggregate(Sum('price')).get('price__sum',0)
            if not week1:
                week1 = 0
            start1 = (week - timedelta(days=week.weekday())).strftime("%b-%d-%Y")
            
            week2 = Bookings.objects.filter(company=company, end__gte=twoweek, end__lte=week).aggregate(Sum('price')).get('price__sum',0)
            if not week2:
                week2 = 0
            start2 = (twoweek - timedelta(days=twoweek.weekday())).strftime("%b-%d-%Y")

            week3 = Bookings.objects.filter(company=company, end__gte=threeweek, end__lte=twoweek).aggregate(Sum('price')).get('price__sum',0)
            if not week3:
                week3 = 0
            start3 = (threeweek - timedelta(days=threeweek.weekday())).strftime("%b-%d-%Y")

            week4 = Bookings.objects.filter(company=company, end__gte=fourweek, end__lte=threeweek).aggregate(Sum('price')).get('price__sum',0)
            if not week4:
                week4 = 0
            start4 = (fourweek - timedelta(days=fourweek.weekday())).strftime("%b-%d-%Y")
            week = [int(week4), int(week3), int(week2), int(week1)]
            weeklabel = [start4, start3, start2, start1]

            month = timezone.now() - timedelta(days=30)
            month1 = Bookings.objects.filter(company=company, end__gte=month, end__lte=timezone.now()).aggregate(Sum('price')).get('price__sum',0)
            if not month1:
                month1 = 0
            labelM0 = timezone.now().strftime("%b-%Y")
            labelM1 = month.strftime("%b-%Y")

            twomonth = month - timedelta(days=30)
            month2 = Bookings.objects.filter(company=company, end__gte=twomonth, end__lte=month).aggregate(Sum('price')).get('price__sum',0)
            if not month2:
                month2 = 0
            labelM2 = twomonth.strftime("%b-%Y")

            threemonth = twomonth - timedelta(days=30)
            month3 = Bookings.objects.filter(company=company, end__gte=threemonth, end__lte=twomonth).aggregate(Sum('price')).get('price__sum',0)
            if not month3:
                month3 = 0
            labelM3 = threemonth.strftime("%b-%Y")

            fourmonth = threemonth - timedelta(days=30)
            month4 = Bookings.objects.filter(company=company, end__gte=fourmonth, end__lte=threemonth).aggregate(Sum('price')).get('price__sum',0)
            if not month4:
                month4 = 0
            labelM4 = fourmonth.strftime("%b-%Y")

            fivemonth = fourmonth - timedelta(days=30)
            month5 = Bookings.objects.filter(company=company, end__gte=fivemonth, end__lte=fourmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month5:
                month5 = 0
            labelM5 = fivemonth.strftime("%b-%Y")

            sixmonth = fivemonth - timedelta(days=30)
            month6 = Bookings.objects.filter(company=company, end__gte=sixmonth, end__lte=fivemonth).aggregate(Sum('price')).get('price__sum',0)
            if not month6:
                month6 = 0
            labelM6 = sixmonth.strftime("%b-%Y")

            sevenmonth = sixmonth - timedelta(days=30)
            month7 = Bookings.objects.filter(company=company, end__gte=sevenmonth, end__lte=sixmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month7:
                month7 = 0
            labelM7 = sevenmonth.strftime("%b-%Y")

            eightmonth = sevenmonth - timedelta(days=30)
            month8 = Bookings.objects.filter(company=company, end__gte=eightmonth, end__lte=sevenmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month8:
                month8 = 0
            labelM8 = eightmonth.strftime("%b-%Y")

            ninemonth = eightmonth - timedelta(days=30)
            month9 = Bookings.objects.filter(company=company, end__gte=ninemonth, end__lte=eightmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month9:
                month9 = 0
            labelM9 = ninemonth.strftime("%b-%Y")

            tenmonth = ninemonth - timedelta(days=30)
            month10 = Bookings.objects.filter(company=company, end__gte=tenmonth, end__lte=ninemonth).aggregate(Sum('price')).get('price__sum',0)
            if not month10:
                month10 = 0
            labelM10 = tenmonth.strftime("%b-%Y")

            elevenmonth = tenmonth - timedelta(days=30)
            month11 = Bookings.objects.filter(company=company, end__gte=elevenmonth, end__lte=tenmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month11:
                month11 = 0
            labelM11 = elevenmonth.strftime("%b-%Y")

            twelvemonth = elevenmonth - timedelta(days=30)
            month12 = Bookings.objects.filter(company=company, end__gte=twelvemonth, end__lte=elevenmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month12:
                month12 = 0
            labelM12 = twelvemonth.strftime("%b-%Y")

            month = [int(month12),int(month11),int(month10),int(month9),int(month8),int(month7),int(month6),int(month5),int(month4),int(month3),int(month2),int(month1),]
            monthlabel = [labelM11,labelM10,labelM9,labelM8,labelM7,labelM6,labelM5,labelM4,labelM3,labelM2,labelM1,labelM0]
            return render(request,'bizadmin/home/home.html', {'ttpp':ttpp,'tpp':tpp,'sdb':sdb,'cdb':cdb,'company':company, 'week':week, 'weeklabel':weeklabel, 'month':month, 'monthlabel':monthlabel, 'bpp':bpp})
        else:
            return redirect(reverse('completeprofile', host='bizadmin'))
    else:
        loginViews(request)

from PIL import Image
from django.core.files import File
from io import BytesIO
from django.core.files.base import ContentFile

#For the main image on the company info
@login_required
def headerImageUpload(request):
    if request.POST:
        company = Company.objects.get(user=request.user)
        img = request.FILES.get('imageFile')
        x = Decimal(request.POST.get('x'))
        y = Decimal(request.POST.get('y'))
        w = Decimal(request.POST.get('width'))
        h = Decimal(request.POST.get('height'))
        valid_extensions = ['jpg', 'png', 'jpeg']
        extension = img.name.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            return redirect(reverse('information', host='bizadmin'))
        if img:
            image = Image.open(img)
            image.filename = img.name
            box = (x, y, w+x, h+y)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((2048,2048),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image.format)
            company.image.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            company.save()
    
    return redirect(reverse('information', host='bizadmin'))

@login_required
def profileImageUpload(request):
    if request.POST:
        user = Account.objects.get(email=request.user)
        img = request.FILES.get('imageFile')
        x = Decimal(request.POST.get('x'))
        y = Decimal(request.POST.get('y'))
        w = Decimal(request.POST.get('width'))
        h = Decimal(request.POST.get('height'))

        valid_extensions = ['jpg', 'png', 'jpeg']
        extension = img.name.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            return redirect(reverse('profile', host='bizadmin'))
        if img:
            image = Image.open(img)
            image.filename = img.name
            box = (x, y, w+x, h+y)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((2048,2048),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image.format)
            user.avatar.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            user.save()
    
    return redirect(reverse('profile', host='bizadmin'))

#For the gallery and photos main photo
@login_required
def headerImageUploads(request):
    if request.POST:
        company = Company.objects.get(user=request.user)
        img = request.FILES.get('imageFile')
        x = Decimal(request.POST.get('x'))
        y = Decimal(request.POST.get('y'))
        w = Decimal(request.POST.get('width'))
        h = Decimal(request.POST.get('height'))
        valid_extensions = ['jpg', 'png', 'jpeg']
        extension = img.name.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            return redirect(reverse('photos', host='bizadmin'))
        if img:
            image = Image.open(img)
            image.filename = img.name
            box = (x, y, w+x, h+y)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((2048,2048),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image.format)
            company.image.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            company.save()
    
    return redirect(reverse('photos', host='bizadmin'))
        
def galImageUpload(request):
    if request.POST:
        company = Company.objects.get(user=request.user)
        img = request.FILES.get('gallaryFile')
        x = Decimal(request.POST.get('xs'))
        y = Decimal(request.POST.get('ys'))
        w = Decimal(request.POST.get('widths'))
        h = Decimal(request.POST.get('heights'))
        valid_extensions = ['jpg', 'png', 'jpeg']
        extension = img.name.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            return redirect(reverse('photos', host='bizadmin'))
        if img:
            image = Image.open(img)
            image.filename = img.name
            box = (x, y, w+x, h+y)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((2048,2048),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, format=image.format)
            gallary = Gallary.objects.create(company=company)
            gallary.photos.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            gallary.save()
    
    return redirect(reverse('photos', host='bizadmin'))

from .forms import ImagesForm
##Business Page Views
@login_required
def businessPhotoView(request):
    company = Company.objects.get(user=request.user)
    photos = Gallary.objects.filter(company=company)
    paginator = Paginator(photos, 6)
    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    return render(request,'bizadmin/businesspage/photos.html',{'company':company, 'photos':photos})

@login_required
def businessAmenitiesView(request):
    company = Company.objects.get(user=request.user)
    amenities = Amenities.objects.filter(company=company)
    return render(request,'bizadmin/businesspage/amenities.html',{'company':company, 'amenities':amenities})

@login_required
def businessHoursView(request):
    company = Company.objects.get(user=request.user)
    sunday = OpeningHours.objects.get(company=company, weekday=0)
    monday = OpeningHours.objects.get(company=company, weekday=1)
    tuesday = OpeningHours.objects.get(company=company, weekday=2)
    wednesday = OpeningHours.objects.get(company=company, weekday=3)
    thursday = OpeningHours.objects.get(company=company, weekday=4)
    friday = OpeningHours.objects.get(company=company, weekday=5)
    saturday = OpeningHours.objects.get(company=company, weekday=6)
    return render(request, 'bizadmin/businesspage/hours.html', {'company':company,'sunday':sunday, 'monday':monday, 'tuesday':tuesday,'wednesday':wednesday, 'thursday':thursday, 'friday':friday, 'saturday':saturday})

class addTagAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['addedTag']
        company = Company.objects.get(user=request.user)
        company.tags.add(tag)
        if not tag:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        return JsonResponse({'tags':'works'})

class removeTagAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['removedTag']
        company = Company.objects.get(user=request.user)
        company.tags.remove(tag)
        if not tag:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        return JsonResponse({'tags':'works'})
from django.contrib.auth import update_session_auth_hash
class updatePassword(View):
    def post(self, request):
        currPass = request.POST.get('currentPassword')
        newPass = request.POST.get('newPassword')
        confirmPass = request.POST.get('confirmPassword')
        user = get_object_or_404(Account, email=request.user)
        if not user.check_password(currPass):
            return JsonResponse({'badresponse':'We could not verify your password. Please try again.'})
        
        if not (newPass==confirmPass):
            return JsonResponse({'badresponse':'Your passwords don\'t match.'})

        if len(newPass)<8 or not any(char.isalpha() for char in newPass) or not any(char.isdigit() for char in newPass):
            return JsonResponse({'badresponse': 'Your password must have atleast 8 characters, 1 digit and 1 letter.'})
        
        user.set_password(newPass)
        user.save()
        update_session_auth_hash(request, user)
        return JsonResponse({'good':'We have changed your password successfully!'})

class changePrivateView(View):
    def post(self, request):
        data = json.loads(request.body)
        privacy = data['private']
        company = get_object_or_404(Company, user=request.user)
        if privacy:
            company.status='draft'
        else:
            company.status='published'
        company.save()
        return JsonResponse({'good':'We updated your privacy settings'})

import string
class addAmenityAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['addedAmenity']
        tag = string.capwords(tag)
        company = Company.objects.get(user=request.user)
        Amenities.objects.create(amenity=tag, company=company)
        if not tag:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        return JsonResponse({'tags':'works'})

class removeAmenityAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['removedAmenity']
        company = Company.objects.get(user=request.user)
        amen = Amenities.objects.get(amenity=tag, company=company)
        amen.delete()

        if not tag:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        return JsonResponse({'tags':'works'})

class deleteGalPic(View):
    def post(self, request):
        data = json.loads(request.body)
        pic_id = data['pics_id']
        company = Company.objects.get(user=request.user)
        picture = Gallary.objects.get(company=company, id=pic_id)
        picture.delete()

        return JsonResponse({'pictures':'pictures'})

@login_required
def compinfoViews(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    
    email = request.user.email
    user = get_object_or_404(Account, email=email)

    if not user.on_board:
        return redirect(reverse('completeprofile', host='bizadmin'))

    company = Company.objects.get(user=user)
    subcategory = company.subcategory.filter(category=company.category)
    s = [x.id for x in subcategory]
    initialVal = {'business_name':company.business_name,'slug':company.slug,'email':company.email,'category':company.category, 'description':company.description,
                    'subcategory':s, 'address':company.address, 'postal':company.postal, 'city':company.city, 'state':company.state,
                    'fb_link':company.fb_link,'twitter_link':company.twitter_link,'instagram_link':company.instagram_link,'website_link':company.website_link,'phone':company.phone}
    updateform = UpdateCompanyForm(initial=initialVal)
    return render(request, 'bizadmin/companydetail/info/compinfo.html', {'company':company, 'updateform': updateform})

import re
#This update form updates the company detail info
class updateCompanyDetail(View):
    def post(self, request):
        data = json.loads(request.body)
        bname = data['name']
        email = data['email']
        phone = data['phone']
        regex= r'^\+?1?\d{9,15}$'
        result = re.match(regex, phone)
        if not bname:
            return JsonResponse({'name_error':'You must include a business name'})
        if (request.user.email!=str(email)) and (Account.objects.filter(email=email).exists()):
            return JsonResponse({'email_error':'This email already exists!'})
        if not result:
            return JsonResponse({'phone_error':'This is not a valid phone number. Please try again'})
        return JsonResponse({'good':'we good'})

class saveCompanyDetail(View):
    def post(self, request):
        category_id = request.POST.get('id_updatecompany-category')
        form = UpdateCompanyForm(request.POST, initial={'category':category_id})
        context = {}
        if form.is_valid():
            company = Company.objects.get(user=request.user)
            company.business_name = form.cleaned_data.get('business_name')
            company.category = form.cleaned_data.get('category')
            subcategory = form.cleaned_data.get('subcategory')
            email = form.cleaned_data.get('email')
            subdomain = request.POST.get('subdomain', company.slug)
            if not email==company.email:
                company.email = email
            phone = form.cleaned_data.get('phone')
            if not phone == company.phone:
                company.phone = phone
            if subdomain != company.slug:
                if not Company.objects.filter(slug=subdomain).exists():
                    company.slug = slugify(subdomain)
            company.description = form.cleaned_data.get('description')
            company.address = form.cleaned_data.get('address')
            company.postal = form.cleaned_data.get('postal')
            company.city = form.cleaned_data.get('city')
            company.province = form.cleaned_data.get('province')
            company.website_link = form.cleaned_data.get('website_link')
            fb = form.cleaned_data.get('fb_link')
            company.fb_link =fb
            company.twitter_link = form.cleaned_data.get('twitter_link')
            company.instagram_link = form.cleaned_data.get('instagram_link')
            company.save()
            subcat = company.subcategory.all()
            for s in subcat:
                company.subcategory.remove(s)
            for s in subcategory:
                company.subcategory.add(s)
            return JsonResponse({'good':'We have saved your company information!'})
        else:
            return JsonResponse({'errors':'Please double check your form. There may be errors.'})

def bookingSettingViews(request):
    company = get_object_or_404(Company, user=request.user)
    bookingform = BookingSettingForm(initial={'interval':company.interval, 'cancellation':company.cancellation})
    return render(request, 'bizadmin/dashboard/account/booking.html', {'company':company, 'booking_form':bookingform})

class bookingAPI(View):
    def post(self, request):
        bookForm = BookingSettingForm(request.POST)
        if bookForm.is_valid():
            company =  get_object_or_404(Company, user=request.user)
            interval = bookForm.cleaned_data.get('interval')
            cancellation = bookForm.cleaned_data.get('cancellation')
            company.interval = interval
            company.cancellation = cancellation
            company.save()
            return JsonResponse({'title':'', 'icon':'error'})
        else:
            return JsonResponse({'title':'Unfortunately, there was an error that occured. Please try again.', 'icon':'error'})

class returningAPI(View):
    def post(self, request):
        data = json.loads(request.body)
        returning = data['returning']
        company = get_object_or_404(Company, user=request.user)
        company.returning = returning
        company.save()
        return JsonResponse({'good':'good'})


def servicesDetailView(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if not user.on_board:
        return redirect(reverse('completeprofile', host='bizadmin'))

    company = Company.objects.get(user=user)
    services = Services.objects.filter(business=company)
    paginator = Paginator(services, 5)
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        services = paginator.page(1)
    except EmptyPage:
        services = paginator.page(paginator.num_pages)
    service_form = AddServiceForm()
    return render(request,'bizadmin/companydetail/services/service.html', {'page':page,'company':company, 'services':services, 'service_form':service_form})

from itertools import chain

def clientListView(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if not user.on_board:
        return redirect(reverse('completeprofile', host='bizadmin'))
    
    company = Company.objects.get(user=user)
    clients = company.clients.all()
    form = AddClientForm()
    return render(request,'bizadmin/companydetail/client/clients.html', {'company':company, 'clients':clients, 'form':form})

from django import template

register = template.Library()

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)

@login_required
def reviewListView(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if not user.on_board:
        return redirect(reverse('completeprofile', host='bizadmin'))
    
    company = Company.objects.get(user=user)
    reviews = Reviews.objects.filter(company=company)
    paginator = Paginator(reviews, 10)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    return render(request,'bizadmin/dashboard/reviews/reviews.html', {'page':page,'company':company, 'reviews':reviews})

@login_required
def requestListViews(request):
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if not user.is_business:
        return redirect(reverse('home', host='bizadmin'))
    if not user.on_board:
        return redirect(reverse('completeprofile', host='bizadmin'))
    company = Company.objects.get(user=user)
    requested = CompanyReq.objects.filter(company=company).order_by('-created_at')

    paginator = Paginator(requested, 10)
    page = request.GET.get('page')
    try:
        requested = paginator.page(page)
    except PageNotAnInteger:
        requested = paginator.page(1)
    except EmptyPage:
        requested = paginator.page(paginator.num_pages)

    return render(request, 'bizadmin/dashboard/request/request.html',{'page':page,'company':company, 'requested':requested})

class getBooking(View):
    def get(self, request):
        company = get_object_or_404(Company, user=request.user)
        booking_id = request.GET.get('booking_id')
        booking = Bookings.objects.get(id=booking_id)
        service = booking.service
        if booking.user:
            user = booking.user
            htmlString = render_to_string('bizadmin/dashboard/schedule/bookingInfo.html',{'user':user, 'booking':booking})
            first_name = user.first_name
            last_name = user.last_name
        else:
            htmlString = render_to_string('bizadmin/dashboard/schedule/bookingInfo.html',{'user':booking.guest, 'booking':booking})
        return JsonResponse({'html_string':htmlString})

class addRequestedViews(View):
    def post(self, request, pk):
        req = get_object_or_404(CompanyReq, id=pk)
        user = req.user
        company = get_object_or_404(Company, user= request.user)
        Clients.objects.create(company=company, user=user, first_name=user.first_name, last_name=user.last_name, email=user.email,phone=user.phone,
                                city=user.city,postal=user.postal,province=user.province,address=user.address)
        addedOnCompanyList.delay(user.id, company.id)
        req.delete()
        requested = company.reqclients.all()
        paginator = Paginator(requested, 10)
        page = request.GET.get('page')
        try:
            requested = paginator.page(page)
        except PageNotAnInteger:
            requested = paginator.page(1)
        except EmptyPage:
            requested = paginator.page(paginator.num_pages)
        html_string = render_to_string('bizadmin/dashboard/request/partial/partial_request.html', {'requested':requested, 'page':page})

        return JsonResponse({'added':'We have added ' + user.first_name + ' to your client list.','html_string':html_string})

class deleteRequestedViews(View):
    def post(self, request, pk):
        req = get_object_or_404(CompanyReq, id=pk)
        user = req.user
        req.delete()
        company = get_object_or_404(Company, user= request.user)
        requested = company.reqclients.all()
        paginator = Paginator(requested, 10)
        page = request.GET.get('page')
        try:
            requested = paginator.page(page)
        except PageNotAnInteger:
            requested = paginator.page(1)
        except EmptyPage:
            requested = paginator.page(paginator.num_pages)
        html_string = render_to_string('bizadmin/dashboard/request/partial/partial_request.html', {'requested':requested, 'page':page})

        return JsonResponse({'deleted':'We have rejected ' + user.first_name + '\'s request to join your client list.','html_string':html_string})
import celery
class deleteBookingByCompAPI(View):
    def post(self, request):
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Bookings, id=booking_id)
        try:
            email = booking.user.email
            appointmentCancelled.delay(booking.id)
        except AttributeError:
            try:
                email = booking.guest.email
                appointmentCancelled.delay(booking.id)
            except AttributeError:
                email = ''
            
        #Dont delete the object, we instead have it on file and change it to cancelled appt
        booking.is_cancelled_company = True
        booking.save()
        return JsonResponse({'':''})

from django.core.exceptions import ObjectDoesNotExist
class addBooking(View):
    def post(self, request):
        company = Company.objects.get(user=request.user)
        bform = AddBookingForm(request.POST,initial={'company':company})
        if bform.is_valid():
            first_name = bform.cleaned_data.get('first_name')
            last_name = bform.cleaned_data.get('last_name')
            email = bform.cleaned_data.get('email')
            phone = bform.cleaned_data.get('phone')
            service = bform.cleaned_data.get('service')
            dur_hour = int(bform.cleaned_data.get('duration_hour'))
            dur_min = int(bform.cleaned_data.get('duration_minute'))
            price = bform.cleaned_data.get('price')
            date = bform.cleaned_data.get('datepick')
            time = bform.cleaned_data.get('timepick')
            start = timezone.localtime(timezone.make_aware(datetime.combine(date, time)))
            end = timezone.localtime(start + timedelta(hours=dur_hour, minutes=dur_min))
            if not email:
                email = None
            if not phone:
                phone = None
            try: 
                guest = company.clients.get(first_name=first_name,last_name=last_name,email=email,phone=phone)
            except ObjectDoesNotExist:
                guest = Clients.objects.create(company=company, first_name=first_name,last_name=last_name, phone=phone, email=email)

            try:
                user = guest.user
            except ObjectDoesNotExist:
                user = None

            booking = Bookings.objects.create(user=user, guest=guest,service=service, company=company,start=start, end=end, price=price)
            booking.save()
            confirmedEmail.delay(booking.id)
            startTime = start - timedelta(minutes=company.confirmation_minutes)
            reminderEmail.apply_async(args=[booking.id], eta=startTime, task_id=booking.slug)
            #Create the booking and then send an email to customer and company
        else:
            day = datetime.today().weekday() + 1
            if day >= 7:
                day = 0
            openhour = OpeningHours.objects.get(company=company, weekday=day).from_hour
            bookings = Bookings.objects.filter(company=company, is_cancelled_user=False, is_cancelled_company=False)
            return render(request, 'bizadmin/dashboard/schedule.html', {'company':company, 'bookings':bookings, 'addbooking':bform, 'errorshow':True})
        return redirect(reverse('schedule', host='bizadmin'))

def load_duration(request):
    service_id = request.GET.get('service_id')
    if service_id:
        service = Services.objects.get(id=service_id)
        hour = service.duration_hour
        mins = service.duration_minute
        price = service.price
    else:
        hour = 1
        mins = 0
        price = 0
    return JsonResponse({'hour':hour,'mins':mins, 'price':price})

def load_client(request):
    client_id = request.GET.get('client_id')
    if client_id:
        client = Clients.objects.get(id=client_id)
        first_name = client.first_name
        last_name = client.last_name
        email = client.email
        phone = client.phone
    else:
        first_name = None
        last_name = None
        email = None
        phone = None
    return JsonResponse({'first_name':first_name,'last_name':last_name, 'email':email,'phone':phone})

#Load the schedule
class load_events(View):
    def get(self, request):
        start = request.GET.get('start')
        end = request.GET.get('end')
        company= Company.objects.get(user=request.user)
        bookings = Bookings.objects.filter(start__gte=start, end__lte=end, company=company, is_cancelled_user=False, is_cancelled_company=False).values()
        bookings_list = list(bookings)

        return JsonResponse(bookings_list, safe=False)

class load_service(View):
    def get(self, request):
        service_id = request.GET.get('service_id')
        services = Services.objects.get(pk=service_id)
        name = services.name
        someStr = 'Service: ' + name
        return JsonResponse({'servName':someStr})
