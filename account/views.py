from .tasks import bizCreatedEmailSent, consumerCreatedEmailSent
from django.shortcuts import render, redirect, get_object_or_404
from .forms import  ConsumerRegistrationForm, AccountAuthenticationForm, UpdatePersonalForm, UpdateHomeAddressForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group, Group
from business.models import Company, Services, Category
from business.forms import SearchForm
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from .models import Account
from business.forms import AddCompanyForm
from bootstrap_modal_forms.generic import (
    BSModalUpdateView
)
from django.views import View
from django.urls import reverse_lazy
from django.http import JsonResponse
import json
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AccountSerializer
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from consumer.models import Reviews
# Create your views here.

def ConsumerRegistrationView(request):
    context = {}
    category = None
    categories = Category.objects.all()
    form = SearchForm()
    Search = None
    results = []
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            results = Company.objects.annotate(search=SearchVector('user','description'),).filter(search=Search)
            return render(request,'business/company/list.html',{'category':category, 'categories':categories ,'companies':results, 'form':form})

    if request.method == 'POST':
        user_form = ConsumerRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            email = user_form.cleaned_data.get('email')
            raw_pass = user_form.cleaned_data.get('password1')
            rmrme = request.POST.get('rememberPasswordCheck')
            
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            if not rmrme:
                request.session.set_expiry(0)
            
            consumerCreatedEmailSent.delay(account.id)

            return redirect('account:registered')
        else:
            context['consumer_registration_form'] = user_form
            
    else:
        user_form = ConsumerRegistrationForm()
        context['consumer_registration_form'] = user_form
    return render(request, 'account/signup.html', {'user_form':user_form, 'category':category, 'categories':categories ,'companies':results, 'form':form})

@login_required
def AccountSummaryView(request):
    acct = get_object_or_404(Account, email=request.user.email)
    category = None
    categories = Category.objects.all()
    form = SearchForm()
    context={}

    if not request.user.is_authenticated:
        return redirect("login")

    personal_data = {'first_name': acct.first_name, 
                    'last_name': acct.last_name, 
                    'email':acct.email, 
                    'phone':acct.phone}

    address_data = {'address': acct.address,
                    'province':acct.province,
                    'city':acct.city,
                    'postal':acct.postal}
    if request.method=='POST':
        if request.POST.get("form_type") == 'personalForm':
            personal_form = UpdatePersonalForm(request.POST, instance=request.user)
            address_form = UpdateHomeAddressForm(initial=address_data)
            if personal_form.is_valid():
                acct.first_name = personal_form.cleaned_data.get('first_name')
                acct.last_name = personal_form.cleaned_data.get('last_name')
                acct.email = personal_form.cleaned_data.get('email')
                acct.phone = personal_form.cleaned_data.get('phone')
                acct.save()
                return redirect('account:account')
            else:
                context['update_personal_form'] = personal_form
        else:
            address_form = UpdateHomeAddressForm(request.POST)
            personal_form = UpdatePersonalForm(initial=personal_data)
            if address_form.is_valid():
                acct.address = address_form.cleaned_data.get('address')
                acct.postal = address_form.cleaned_data.get('postal')
                acct.city = address_form.cleaned_data.get('city')
                acct.province = address_form.cleaned_data.get('province')
                acct.save()
                return redirect('account:account')
            else:
                context['update_address_form'] = address_form
    else:
        personal_form = UpdatePersonalForm(initial=personal_data)
        address_form = UpdateHomeAddressForm(initial=address_data)

    context['update_personal_form'] = personal_form
    context['update_address_form'] = address_form

    return render(request, 'account/cons_account_information.html', {'personal_form':personal_form,'address_form':address_form,'acct':acct, 'category':category, 'categories':categories , 'form':form})

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
            rmrme = request.POST.get('rememberPasswordCheck')
            
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if not rmrme:
                    request.session.set_expiry(0)
                return redirect('business:homepage')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    search = SearchForm()
    return render(request, 'registration/login.html', {'login_form':form, 'form':search})

def SignUpView(request):
    return render(request, 'account/signup.html')

@login_required
def BusinessListViews(request):
    if not request.user.is_authenticated:
        return redirect("login")
    companies = Company.objects.all()
    companies = companies.filter(user=request.user)
    return render(request, 'account/company_page_list.html', {'my_companies':companies})

@login_required
def homeAddressChangeView(request):
    context={}
    email = request.user.email
    user = Account.objects.get(email=email)
    data = {'address': user.address}
    if request.method == 'POST':
        user_form = UpdateHomeAddressForm(request.POST)
        if user_form.is_valid():
            user.address = user_form.cleaned_data.get('address')
            user.save()
            return redirect('account:account')
        else:
            context['update_home_form'] = user_form
            
    else:
        user_form = UpdateHomeAddressForm(initial=data)
        context['update_home_form'] = user_form
    return render(request, 'account/consumer/home_update.html', {'update_form':user_form, 'user':user})

@api_view(['GET'])
def accountList(request):
    acct = Account.objects.get(email=request.user.email)
    serializer = AccountSerializer(acct, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def accountUpdate(request):
    acct = Account.objects.get(email=request.user.email)
    serializer = AccountSerializer(instance=acct,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

class personalValidationView(View):
    def post(self, request):
        data=json.loads(request.body)
        email = data['email']
        phone = data['phone']
        regex= r'^\+?1?\d{9,15}$'
        result = re.match(regex, phone)
        if not phone:
            result = True
        if (request.user.email!=str(email)) and (Account.objects.filter(email=email).exists()):
            return JsonResponse({'email_error':'This email already exists!'}, status=409)
        if not (result):
            return JsonResponse({'phone_error':'Please enter a valid phone number.'}, status=409)
        return JsonResponse({'email_valid':True})

def favouriteViews(request):
    companies = request.user.companies_liked.all()
    form = SearchForm()
    paginator = Paginator(companies, 6)
    page = request.GET.get('page')
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)
    return render(request, 'account/favorite.html', {'companies':companies, 'page':page, 'form':form})

def reviewsViews(request):
    reviews = Reviews.objects.filter(reviewer=request.user)
    form = SearchForm()
    paginator = Paginator(reviews, 6)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    return render(request, 'account/reviews.html', {'reviews':reviews, 'page':page, 'form':form})
