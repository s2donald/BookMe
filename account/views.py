from django.shortcuts import render, redirect
from .forms import  BusinessRegistrationForm, ConsumerRegistrationForm, AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group, Group
from business.models import Company, Services, Category
from business.forms import SearchForm
from django.contrib.postgres.search import SearchVector
from business.views import searchBarView
# Create your views here.

def ConsumerRegistrationView(request):
    context = {}
    searchBar = searchBarView(request)
    category = searchBar[0]
    categories = searchBar[1]
    results = searchBar[2]
    form = searchBar[3]
    if request.method == 'POST':
        user_form = ConsumerRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
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
    return render(request, 'account/consumer/registration.html', {'user_form':user_form, 'category':category, 'categories':categories ,'companies':results, 'form':form})


def BusinessRegistrationView(request):
    context = {}
    if request.method == 'POST':
        user_form = BusinessRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
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
    if not request.user.is_authenticated:
        return redirect("login")

    is_bus = request.user.is_business
    if is_bus:
        my_company = Company.objects.get(user=request.user)
        return render(request, 'account/account_information.html', {'company':my_company})
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