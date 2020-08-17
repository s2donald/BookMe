from .tasks import bizaddedEmailSent
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
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
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
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            return redirect('account:registered')
        else:
            context['consumer_registration_form'] = user_form
            
    else:
        user_form = ConsumerRegistrationForm()
        context['consumer_registration_form'] = user_form
    return render(request, 'account/signup.html', {'user_form':user_form, 'category':category, 'categories':categories ,'companies':results, 'form':form})


# def BusinessRegistrationView(request):
#     context = {}
#     category = None
#     categories = Category.objects.all()
#     form = SearchForm()
#     Search = None
#     results = []
#     if 'Search' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             Search = form.cleaned_data['Search']
#             results = Company.objects.annotate(search=SearchVector('user','description'),).filter(search=Search)
#             return render(request,'business/company/list.html',{'category':category, 'categories':categories ,'companies':results, 'form':form})

#     if request.method == 'POST':
#         user_form = BusinessRegistrationForm(request.POST)
#         if user_form.is_valid():
#             user_form.save()
#             email = user_form.cleaned_data.get('email')
#             raw_pass = user_form.cleaned_data.get('password1')
#             account = authenticate(email=email, password=raw_pass)
#             login(request, account)
#             return redirect('account:registered')
#         else:
#             context['business_registration_form'] = user_form
            
#     else:
#         user_form = BusinessRegistrationForm()
#         context['business_registration_form'] = user_form
#     return render(request, 'account//business/registration.html', {'user_form':user_form, 'category':category, 'categories':categories ,'companies':results, 'form':form})
@login_required
def AccountSummaryView(request):
    acct = get_object_or_404(Account, email=request.user.email)
    category = None
    categories = Category.objects.all()
    companies = Company.objects.all().filter(user=request.user)
    form = SearchForm()
    Search = None
    results = []
    context={}
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            results = Company.objects.annotate(search=SearchVector('user','description'),).filter(search=Search)
            return render(request,'business/company/list.html',{'category':category, 'categories':categories ,'companies':results, 'form':form})

    if not request.user.is_authenticated:
        return redirect("login")

    personal_data = {'first_name': acct.first_name, 
                    'last_name': acct.last_name, 
                    'email':acct.email, 
                    'phone':acct.phone}

    address_data = {'address': acct.address}
    if request.method=='POST':
        if request.POST.get("form_type") == 'personalForm':
            personal_form = UpdatePersonalForm(request.POST)
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
                acct.save()
                return redirect('account:account')
            else:
                context['update_address_form'] = address_form
    else:
        personal_form = UpdatePersonalForm(initial=personal_data)
        address_form = UpdateHomeAddressForm(initial=address_data)

    context['update_personal_form'] = personal_form
    context['update_address_form'] = address_form

    return render(request, 'account/cons_account_information.html', {'personal_form':personal_form,'address_form':address_form,'acct':acct,'my_companies':companies, 'category':category, 'categories':categories ,'companies':results, 'form':form})

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

@login_required
def addBusinessView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    context={}
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if request.method == 'POST':
        user_form = AddCompanyForm(request.POST)
        if user_form.is_valid():
            business_name = user_form.cleaned_data.get('business_name')
            category = user_form.cleaned_data.get('category')
            description = user_form.cleaned_data.get('description')
            address = user_form.cleaned_data.get('address')
            postal = user_form.cleaned_data.get('postal')
            state = user_form.cleaned_data.get('state')
            city = user_form.cleaned_data.get('city')
            status = user_form.cleaned_data.get('status')
            company = Company.objects.create(user=user,business_name=business_name,category=category,
                                                description=description,address=address,postal=postal,
                                                state=state,city=city,status=status)
            company.save()
            user_id = user.id
            bizaddedEmailSent.delay(user_id)
            return redirect('account:account')
        else:
            context['user_form'] = user_form
    else:
        user_form = AddCompanyForm()
        context['user_form'] = user_form
    
    return render(request,'account/add_page.html', {'biz_form':user_form})

@login_required
def BusinessListViews(request):
    if not request.user.is_authenticated:
        return redirect("login")
    companies = Company.objects.all()
    companies = companies.filter(user=request.user)
    return render(request, 'account/company_page_list.html', {'my_companies':companies})

@login_required
def BusinessAccountsView(request, id, slug):
    if not request.user.is_authenticated:
        return redirect("login")
    companies = Company.objects.filter(user=request.user)
    company = get_object_or_404(Company, id=id, slug=slug, available=True)
    services = Services.objects.filter(business=company)
    return render(request, 'business/company/manage/service/manage_service_list.html', {'services':services,'company':company, 'companies':companies})

@login_required
def NameChangeView(request):
    context={}
    email = request.user.email
    user = Account.objects.get(email=email)
    data = {'first_name': user.first_name, 'last_name':user.last_name}
    if request.method == 'POST':
        user_form = UpdateNameForm(request.POST)
        if user_form.is_valid():
            user.first_name = user_form.cleaned_data.get('first_name')
            user.last_name = user_form.cleaned_data.get('last_name')
            user.save()
            return redirect('account:account')
        else:
            context['user_form'] = user_form
            
    else:
        user_form = UpdateNameForm(initial=data)
        context['user_form'] = user_form
    return render(request, 'account/consumer/name_update.html', {'update_form':user_form, 'user':user})

@login_required
def emailChangeView(request):
    context={}
    email = request.user.email
    user = Account.objects.get(email=email)
    data = {'email': user.email}
    if request.method == 'POST':
        user_form = UpdateEmailForm(request.POST)
        if user_form.is_valid():
            user.email = user_form.cleaned_data.get('email')
            user.save()
            return redirect('account:account')
        else:
            context['update_name_form'] = user_form
            
    else:
        user_form = UpdateEmailForm(initial=data)
        context['update_name_form'] = user_form
    return render(request, 'account/consumer/email_update.html', {'update_form':user_form, 'user':user})

# def save_information_form(request, form, template_name):
#     data = dict()
#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             data['form_is_valid'] = True
#             account = Account.objects.get(email=request.user.email)
#             data['html_account_info'] = render_to_string('account/cons_account_information.html', {'account':account})
#         else:
#             data['form_is_valid'] = False
#     context = {'form':form}
#     data['html_form'] = render_to_string(template_name, context, request=request)
#     return JsonResponse(data)


# @login_required
# def emailUpdateView(request):
#     if request.method=='POST':
#         form = UpdateEmailForm(request.POST)
#     else:
#         form = UpdateEmailForm()
#     return save_information_form(request, form, 'account/consumer/email_update.html')

@login_required
def phoneChangeView(request):
    context={}
    email = request.user.email
    user = Account.objects.get(email=email)
    data = {'phone': user.phone}
    if request.method == 'POST':
        user_form = UpdatePhoneForm(request.POST)
        if user_form.is_valid():
            user.phone = user_form.cleaned_data.get('phone')
            user.save()
            return redirect('account:account')
        else:
            context['update_phone_form'] = user_form
            
    else:
        user_form = UpdatePhoneForm(initial=data)
        context['update_phone_form'] = user_form
    return render(request, 'account/consumer/phone_update.html', {'update_form':user_form, 'user':user})

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