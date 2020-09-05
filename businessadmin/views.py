from django.shortcuts import render, get_object_or_404, redirect
from .forms import BusinessRegistrationForm
from django.contrib.auth.decorators import login_required
from business.models import Company, SubCategory
from account.models import Account
from account.tasks import bizaddedEmailSent
from consumer.models import Bookings
from account.forms import AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django_hosts.resolvers import reverse
from django.http import JsonResponse
from business.forms import AddCompanyForm, AddServiceForm
# Create your views here.
def businessadmin(request):
    user = request.user
    business = False
    if user.is_authenticated and user.is_business:
        business = True

    return render(request, 'welcome/welcome.html', {'business':business})

def pricingViews(request):
    return render(request, 'welcome/pricing.html')

def faqBusinessViews(request):
    return render(request, 'welcome/faq.html')

def completeViews(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    company = Company.objects.filter(user=user)
    if company:
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
            company = Company.objects.create(user=user,business_name=business_name,category=category,
                                                description=description,address=address,postal=postal,
                                                state=state,city=city,status=status, avgrating=0)
            for s in subcategory:
                company.subcategory.add(s)
            bookings = Bookings.objects.filter(company=company)
            return render(request, 'bizadmin/dashboard/schedule.html', {'company':company, 'bookings':bookings})

        
            # user_id = user.id
            # bizaddedEmailSent.delay(user_id)

    biz_form = AddCompanyForm()
    service_form = AddServiceForm()
    subcategories = SubCategory.objects.all()
    return render(request, 'bizadmin/dashboard/profile/addcompany.html', {'biz_form':biz_form, 'service_form':service_form,'subcategories':subcategories})

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
            return redirect(reverse('completeprofile', host='bizadmin'))
        else:
            context['business_registration_form'] = user_form
            
    else:
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
    return render(request, 'account/bussignup.html', {'user_form':user_form})

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
                    company = Company.objects.filter(user=account)
                    if company:
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
    return render(request, 'account/buslogin.html', {'user_form':user_form})

def profileViews(request):
    return render(request, 'bizadmin/dashboard/account/profile.html')

def profileBillingViews(request):
    return render(request,'bizadmin/dashboard/account/billing.html')

def profileSecurityViews(request):
    return render(request,'bizadmin/dashboard/account/security.html')

@login_required
def scheduleView(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        company = Company.objects.get(user=user)
        if company:
            bookings = Bookings.objects.filter(company=company)
            return render(request, 'bizadmin/dashboard/schedule.html', {'company':company, 'bookings':bookings})
        else:
            return redirect(reverse('completeprofile', host='bizadmin'))
    else:
        loginViews()

def fileUploadView(request):
    if request.POST:
        return JsonResponse({'works':'works'})


    