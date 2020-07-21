from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Company, Services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm, AddServiceForm, UpdateServiceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import generic


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
            results = Company.objects.annotate(search=SearchVector('business_name','description'),).filter(search=Search)
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
            results = Company.objects.annotate(search=SearchVector('business_name','description'),).filter(search=Search)
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
    address = company.address
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
    return render(request, 'business/company/detail.html', {'address':address,'company':company,'category':category,'categories':categories, 'services':services, 'form':form})

@login_required
def ManageServiceListView(request, id, slug):
    category = None
    categories = Category.objects.all()
    

    is_biz = request.user.is_business
    if is_biz:
        company = get_object_or_404(Company, user=request.user, id=id, slug=slug)
        services = Services.objects.all().filter(business=company)
        return render(request, 'business/company/manage/service/manage_service_list.html', {'services':services, 'company':company, 'category':category,'categories':categories})

@login_required
def CreateServiceView(request, pk, slug):
    context = {}
    company = get_object_or_404(Company, user=request.user, id=pk, slug=slug)
    if request.method == 'POST':
        service_form = AddServiceForm(request.POST)
        if service_form.is_valid():
            name = service_form.cleaned_data.get('name')
            description = service_form.cleaned_data.get('description')
            price = service_form.cleaned_data.get('price')
            avail = True
            slugname = name + '' + request.user.slug
            service = Services.objects.create(business=company,name=name,description=description,price=price, available=avail, slug=slugname)
            service.save()
            return redirect(reverse('business:manage_service_list', args=[pk, slug]))
        else:
            context['service_form'] = service_form
            
    else:
        service_form = AddServiceForm()
        context['service_form'] = service_form
    return render(request, 'business/company/manage/service/create.html',{'service_form':service_form})


#Remember we must validate everything before deleting
@login_required
def DeleteServiceView(request, pk, pks, slug):
    company = get_object_or_404(Company, user=request.user, id=pks, slug=slug)
    service = Services.objects.get(business=company, id=pk)
    if request.method == 'POST':
        service.delete()
        return redirect(reverse('business:manage_service_list', args=[pks, slug]))
        

    return render(request, 'business/company/manage/service/delete.html',{'service':service})

@login_required
def UpdateServiceView(request, pk, pks, slug):
    context = {}
    company = get_object_or_404(Company, user=request.user, id=pks, slug=slug)
    service = Services.objects.get(business=company, id=pk)
    data = {'name': service.name, 'description': service.description, 'price':service.price, 'available':service.available}
    if request.method == 'POST':
        service_update_form = UpdateServiceForm(request.POST)
        if service_update_form.is_valid():
            name = service_update_form.cleaned_data.get('name')
            description = service_update_form.cleaned_data.get('description')
            price = service_update_form.cleaned_data.get('price')
            serv = Services.objects.get(pk=pk)
            serv.name = name
            serv.description = description
            serv.price = price
            serv.save()
            return redirect(reverse('business:manage_service_list', args=[pks, slug]))
        else:
            context['service_update_form'] = service_update_form
    else:
        service_update_form = UpdateServiceForm(initial=data)
        context['service_update_form'] = service_update_form

    return render(request, 'business/company/manage/service/update.html',{'service':service, 'update_form':service_update_form})