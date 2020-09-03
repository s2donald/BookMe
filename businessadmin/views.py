from django.shortcuts import render, get_object_or_404, redirect
from .forms import BusinessRegistrationForm
from django.contrib.auth.decorators import login_required
from business.models import Company
from consumer.models import Bookings
from account.forms import AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django_hosts.resolvers import reverse
from django.http import JsonResponse
# Create your views here.

def businessadmin(request):
    return render(request, 'welcome/welcome.html')

def pricingViews(request):
    return render(request, 'welcome/pricing.html')

def faqBusinessViews(request):
    return render(request, 'welcome/faq.html')

def completeViews(request):
    return render(request, 'bizadmin/dashboard/profile/addcompany.html')

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
            return redirect('businessadmin:completeprofile')
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
                return redirect(reverse('schedule', host='bizadmin'))
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
        bookings = Bookings.objects.filter(company=company)
        return render(request, 'bizadmin/dashboard/schedule.html', {'company':company, 'bookings':bookings})
    else:
        loginViews()

def fileUploadView(request):
    if request.POST:
        return JsonResponse({'works':'works'})


    