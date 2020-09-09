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
from business.forms import AddCompanyForm, AddServiceForm, UpdateServiceForm
from django.forms import inlineformset_factory
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
    HoursFormSet = inlineformset_factory(Company, OpeningHours, fields=('from_hour','to_hour','is_closed',))
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if user.on_board:
        return redirect(reverse('schedule', host='bizadmin')) 
    if request.method == 'POST':
        biz_form = AddCompanyForm(request.POST)
        if biz_form.is_valid():
            business_name = biz_form.cleaned_data.get('business_name')
            category = biz_form.cleaned_data.get('category')
            subcategory = biz_form.cleaned_data.get('subcategory')
            description = biz_form.cleaned_data.get('description')
            address = biz_form.cleaned_data.get('address')
            postal = biz_form.cleaned_data.get('postal')
            state = biz_form.cleaned_data.get('state')
            city = biz_form.cleaned_data.get('city')
            status = 'published'
            company = Company.objects.get(user=user)
            company.business_name = business_name
            company.category = category
            company.description = description
            company.address = address
            company.postal = postal
            company.state = state
            company.city = city
            company.status = status
            company.save()
            user.on_board = True
            user.save()
            for s in subcategory:
                company.subcategory.add(s)
            bookings = Bookings.objects.filter(company=company)
            return render(request, 'bizadmin/dashboard/schedule.html', {'company':company, 'bookings':bookings})

        
            # user_id = user.id
            # bizaddedEmailSent.delay(user_id)

    biz_form = AddCompanyForm()
    service_form = AddServiceForm()
    subcategories = SubCategory.objects.all()
    company = Company.objects.get(user=user)
    services = Services.objects.filter(business=company)
    hours = OpeningHours.objects.filter()
    hourFormset = HoursFormSet(instance=company)
    sunday = OpeningHours.objects.get(company=company, weekday=0)
    monday = OpeningHours.objects.get(company=company, weekday=1)
    tuesday = OpeningHours.objects.get(company=company, weekday=2)
    wednesday = OpeningHours.objects.get(company=company, weekday=3)
    thursday = OpeningHours.objects.get(company=company, weekday=4)
    friday = OpeningHours.objects.get(company=company, weekday=5)
    saturday = OpeningHours.objects.get(company=company, weekday=6)

    return render(request, 'bizadmin/dashboard/profile/addcompany.html', {'sunday':sunday,'biz_form':biz_form, 'service_form':service_form,'subcategories':subcategories,'company':company,'services':services, 'hourFormset':hourFormset})

def signupViews(request):
    context = {}
    if request.method == 'POST':
        user_form = BusinessRegistrationForm(request.POST)
        
        if user_form.is_valid():
            user_form.save()
            email = user_form.cleaned_data.get('email')
            raw_pass = user_form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            company = Company.objects.create(user=account,business_name='',
                                                description='',address='',postal='',
                                                state='',city='',status='draft', avgrating=0)
            biz_hours = OpeningHours.objects.bulk_create([
                OpeningHours(company=company, weekday=0,is_closed=True),
                OpeningHours(company=company, weekday=1,is_closed=True),
                OpeningHours(company=company, weekday=2,is_closed=True),
                OpeningHours(company=company, weekday=3,is_closed=True),
                OpeningHours(company=company, weekday=4,is_closed=True),
                OpeningHours(company=company, weekday=5,is_closed=True),
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
    dat = {'name': service.name, 'description': service.description, 'price_type':service.price_type, 'price':service.price, 'available':service.available, 'duration_hour':service.duration_hour, 'duration_minute':service.duration_minute}
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
            service.checkintime=form.cleaned_data.get('checkintime')
            service.padding=form.cleaned_data.get('padding')
            service.paddingtime_hour=form.cleaned_data.get('paddingtime_hour')
            service.paddingtime_minute=form.cleaned_data.get('paddingtime_minute')
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


    