from django.shortcuts import render, redirect, get_object_or_404
from .forms import  ConsumerRegistrationForm, AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, Group, Group
from business.models import Company, Services, Category
from business.forms import SearchForm
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
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
    category = None
    categories = Category.objects.all()
    companies = Company.objects.all()
    companies = companies.filter(user=request.user)
    form = SearchForm()
    Search = None
    results = []
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            results = Company.objects.annotate(search=SearchVector('user','description'),).filter(search=Search)
            return render(request,'business/company/list.html',{'category':category, 'categories':categories ,'companies':results, 'form':form})

    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, 'account/cons_account_information.html', {'my_companies':companies, 'category':category, 'categories':categories ,'companies':results, 'form':form})

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
def BusinessListViews(request):
    companies = Company.objects.all()
    companies = companies.filter(user=request.user)
    return render(request, 'account/company_page_list.html', {'my_companies':companies})

@login_required
def BusinessAccountsView(request, id, slug):
    companies = Company.objects.all().filter(user=request.user)
    company = get_object_or_404(Company, id=id, slug=slug, available=True)
    services = Services.objects.all().filter(business=company)
    return render(request, 'business/company/manage/service/manage_service_list.html', {'services':services,'company':company, 'companies':companies})