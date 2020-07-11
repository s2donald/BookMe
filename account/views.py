from django.shortcuts import render, redirect
from .forms import  BusinessRegistrationForm, ConsumerRegistrationForm, AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group, Group
# Create your views here.


def ConsumerRegistrationView(request):
    context = {}
    if request.method == 'POST':
        user_form = ConsumerRegistrationForm(request.POST)
        if user_form.is_valid():
            #Now save the user and set the password
            user_form.save()
            #new_user.set_password(user_form.cleaned_data['password1'])
            # new_user.username = user_form.cleaned_data['email']
            # new_user.slug = user_form.cleaned_data['business_name']
            # if usertype == 'business':
            #     new_user.is_business = True
            # new_user.save()
            email = user_form.cleaned_data.get('email')
            raw_pass = user_form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            return redirect('account:registered')
        else:
            context['consumer_registration_form'] = user_form
            
    else:
        user_form = ConsumerRegistrationForm()
        context['consumer_registration_form'] = user_form
    return render(request, 'account/consumer/registration.html', {'user_form':user_form})


def BusinessRegistrationView(request):
    context = {}
    if request.method == 'POST':
        user_form = BusinessRegistrationForm(request.POST)
        if user_form.is_valid():
            #Now save the user and set the password
            user_form.save()
            #new_user.set_password(user_form.cleaned_data['password1'])
            # new_user.username = user_form.cleaned_data['email']
            # new_user.slug = user_form.cleaned_data['business_name']
            # if usertype == 'business':
            #     new_user.is_business = True
            # new_user.save()
            email = user_form.cleaned_data.get('email')
            raw_pass = user_form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            return redirect('account:registered')
        else:
            context['business_registration_form'] = user_form
            
    else:
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
    return render(request, 'account//business/registration.html', {'user_form':user_form})

def AccountSummaryView(request):
    is_bus = request.user.is_business
    if is_bus:
        return render(request, 'account/account_information.html')
    return render(request, 'account/cons_account_information.html')

def RegisteredAccountView(request):
    return render(request, 'account/register_done.html')

def LogoutView(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

def LoginView(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('business:homepage')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('business:homepage')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'registration/login.html', {'form':form})

def SignUpView(request):
    return render(request, 'account/signup.html')