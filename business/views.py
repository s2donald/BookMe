from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Company, Services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def searchBarView(request):
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
            return render(request,'business/company/list.html',{'category':category, 'categories':categories ,'companies':results})

    return (category, categories, results, form)
    
# Create your views here.
def homepage(request, category_slug=None):
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
            return render(request, 'business/company/list.html',{'category':category, 'categories':categories ,'companies':results})
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'business/home.html', {'category':category, 'categories':categories, 'form':form})

def company_list(request, category_slug=None, company_slug=None, tag_slug=None):
    category = None
    categories = Category.objects.all()
    companies = Company.objects.all()
    tag=None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        companies = companies.filter(category=category)
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        companies = companies.filter(tags__in=[tag])
    form = SearchForm()
    Search = None
    results = []
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            results = Company.objects.annotate(search=SearchVector('user','description'),).filter(search=Search)
            return render(request, 'business/company/list.html',{'category':category, 'categories':categories ,'companies':results})
    counts = companies.count()%6
    paginator = Paginator(companies, 4)
    page = request.GET.get('page')
    try:
        companiess = paginator.page(page)
    except PageNotAnInteger:
        companiess = paginator.page(1)
    except EmptyPage:
        companiess = paginator.page(paginator.num_pages)
    return render(request, 'business/company/list.html',{'page':page,'category':category, 'companies':companiess, 'categories':categories, 'counts':counts, 'form':form,'tag':tag})

def company_detail(request, id, slug):
    company = get_object_or_404(Company, id=id, slug=slug, available=True)
    category = None
    categories = Category.objects.all()
    services = Services.objects.all().filter(business=company)
    form = SearchForm()
    Search = None
    results = []
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            results = Company.objects.annotate(search=SearchVector('user','description'),).filter(search=Search)
            return render(request, 'business/company/list.html',{'category':category, 'categories':categories ,'companies':results})
    return render(request, 'business/company/detail.html', {'company':company,'category':category,'categories':categories, 'services':services, 'form':form})

@login_required
def ManageServiceListView(request):
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
            return render(request, 'business/company/list.html',{'category':category, 'categories':categories ,'companies':results})

    is_biz = request.user.is_business
    if is_biz:
        company = get_object_or_404(Company, user=request.user)
        services = Services.objects.all().filter(business=company)
        return render(request, 'business/company/manage/service/manage_service_list.html', {'services':services})
