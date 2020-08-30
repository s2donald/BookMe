from django.shortcuts import render
from .forms import BusinessRegistrationForm
# Create your views here.

def businessadmin(request):
    return render(request, 'welcome/welcome.html')

def pricingViews(request):
    return render(request, 'welcome/pricing.html')

def faqBusinessViews(request):
    return render(request, 'welcome/faq.html')


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
            return redirect('businessadmin:nextsteps')
        else:
            context['business_registration_form'] = user_form
            
    else:
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
    return render(request, 'account/bussignup.html')

def loginViews(request):
    return render(request, 'account/buslogin.html')

def profileViews(request):
    return render(request, 'admin/dashboard/account/profile.html')

def profileBillingViews(request):
    return render(request,'admin/dashboard/account/billing.html')

def profileSecurityViews(request):
    return render(request,'admin/dashboard/account/security.html')

def scheduleView(request):
    return render(request, 'admin/dashboard/schedule.html')