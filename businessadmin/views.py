from django.shortcuts import render, get_object_or_404, redirect
from .forms import BusinessRegistrationForm
from django.contrib.auth.decorators import login_required
from business.models import Company, SubCategory, OpeningHours, Services
from account.models import Account
from account.tasks import bizaddedEmailSent
from consumer.models import Bookings
from account.forms import AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django_hosts.resolvers import reverse
from django.http import JsonResponse
import json
from business.forms import AddCompanyForm, AddServiceForm, UpdateServiceForm, BookingSettingForm
from django.forms import inlineformset_factory
from django.views import View
from slugify import slugify

# Create your views here.
def businessadmin(request):
    user = request.user
    business = False
    if user.is_authenticated and user.is_business:
        business = True

    return render(request, 'welcome/welcome.html', {'business':business, 'none':'d-none'})

def pricingViews(request):
    user = request.user
    business = False
    if user.is_authenticated and user.is_business:
        business = True
    return render(request, 'welcome/pricing.html', {'business':business,'none':'d-none'})

def faqBusinessViews(request):
    user = request.user
    business = False
    if user.is_authenticated and user.is_business:
        business = True
    return render(request, 'welcome/faq.html', {'business':business,'none':'d-none'})

def completeViews(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    
    if user.on_board:
        return redirect(reverse('schedule', host='bizadmin')) 
    print('hellofromtype')
    if request.method == 'POST':
        biz_form = AddCompanyForm(request.POST)
        booking_form = BookingSettingForm(request.POST)
        print(biz_form)
        if biz_form.is_valid() and booking_form.is_valid():
            company = Company.objects.get(user=user)
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
            subdomain = request.POST.get('subdomain',company.slug)
            sun_from = request.POST['sunOpenHour']
            sun_to = request.POST['sunCloseHour']
            sun_closed = not request.POST.get('sunOpen', False)
            mon_from = request.POST['monOpenHour']
            mon_to = request.POST['monCloseHour']
            mon_closed = not request.POST.get('monOpen', False)
            tues_from = request.POST['tuesCloseHour']
            tues_to = request.POST['tuesOpenHour']
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

            status = 'published'
            company.category = category
            company.description = description
            company.address = address
            company.postal = postal
            company.state = state
            company.city = city
            company.status = status
            company.interval = interval
            company.notes = notes
            company.cancellation = cancellation
            if subdomain != company.slug:
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

            objs[0].from_hour = sun_from
            objs[1].from_hour = mon_from
            objs[2].from_hour = tues_from
            objs[3].from_hour = wed_from
            objs[4].from_hour = thurs_from
            objs[5].from_hour = fri_from
            objs[6].from_hour = sat_from

            objs[0].to_hour = sun_to
            objs[1].to_hour = mon_to
            objs[2].to_hour = tues_to
            objs[3].to_hour = wed_to
            objs[4].to_hour = thurs_to
            objs[5].to_hour = fri_to
            objs[6].to_hour = sat_to

            OpeningHours.objects.bulk_update(objs,['is_closed','from_hour','to_hour'])
            for s in subcategory:
                company.subcategory.add(s)
            bookings = Bookings.objects.filter(company=company)
            return render(request, 'bizadmin/dashboard/schedule.html', {'company':company, 'bookings':bookings})

        
            # user_id = user.id
            # bizaddedEmailSent.delay(user_id)

    biz_form = AddCompanyForm()
    service_form = AddServiceForm()
    booking_form = BookingSettingForm()
    subcategories = SubCategory.objects.all()
    company = Company.objects.get(user=user)
    services = Services.objects.filter(business=company)
    sunday = OpeningHours.objects.get(company=company, weekday=0)
    monday = OpeningHours.objects.get(company=company, weekday=1)
    tuesday = OpeningHours.objects.get(company=company, weekday=2)
    wednesday = OpeningHours.objects.get(company=company, weekday=3)
    thursday = OpeningHours.objects.get(company=company, weekday=4)
    friday = OpeningHours.objects.get(company=company, weekday=5)
    saturday = OpeningHours.objects.get(company=company, weekday=6)

    return render(request, 'bizadmin/dashboard/profile/addcompany.html', {'booking_form':booking_form,'sunday':sunday,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday,'saturday':saturday,
                                                                                'biz_form':biz_form, 'service_form':service_form,'subcategories':subcategories,'company':company,
                                                                                'services':services})

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
            bname = request.POST.get('bname', '')
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            company = Company.objects.create(user=account,business_name=bname,
                                                description='',address='',postal='',
                                                state='',city='',status='draft', avgrating=0)
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
                        return redirect(reverse('schedule', host='bizadmin'))
                    else:
                        return redirect(reverse('completeprofile', host='bizadmin'))
                        
                else:
                    return redirect(reverse('notbusiness', host='bizadmin'))
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
            return render(request, 'bizadmin/dashboard/account/profile.html',{'company':company})
        else:
            return redirect(reverse('completeprofile', host='bizadmin'))
    else:
        loginViews(request)
    

def profileBillingViews(request):
    return render(request,'bizadmin/dashboard/account/billing.html')

def profileSecurityViews(request):
    return render(request,'bizadmin/dashboard/account/security.html')

@login_required
def scheduleView(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            bookings = Bookings.objects.filter(company=company)
            return render(request, 'bizadmin/dashboard/schedule.html', {'company':company, 'bookings':bookings})
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
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
    
    context = {'service_form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def createserviceViews(request):
    if request.method=='POST':
        service_form = AddServiceForm(request.POST)
    else:
        service_form = AddServiceForm()
    return save_service_form(request, service_form, 'bizadmin/dashboard/profile/services/partial_service_create.html')

def deleteserviceViews(request, pk):

    company = Company.objects.get(user=request.user)
    service = get_object_or_404(Services, pk=pk, business=company)
    data = dict()
    if request.method=='POST':
        service.delete()
        data['form_is_valid']=True
        services = Services.objects.filter(business=company)
        data['html_service_list'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_list.html', {'services':services})
    else:
        context = {'service':service}
        data['html_form'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_delete.html', context, request=request)
    return JsonResponse(data)

def updateserviceViews(request, pk):
    service = get_object_or_404(Services, pk=pk)
    company = Company.objects.get(user=request.user)
    dat = {'name': service.name, 'description': service.description, 'price_type':service.price_type, 'price':service.price, 'available':service.available, 'duration_hour':service.duration_hour, 'duration_minute':service.duration_minute, 'checkintime':service.checkintime, 'padding':service.padding, 'paddingtime_hour':service.paddingtime_hour, 'paddingtime_minute':service.paddingtime_minute}
    data=dict()
    if request.method=='POST':
        form = UpdateServiceForm(request.POST)
        print(form)
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
            data['html_service_list'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_list.html', {'services':services})
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
    else:
        form = UpdateServiceForm(initial=dat)
    context = {'service_form':form, 'service':service}
    data['html_form'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_update.html', context, request=request)
    return JsonResponse(data)


    