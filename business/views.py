from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Company, Services, SubCategory, Amenities, OpeningHours, Gallary
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm, AddServiceForm, UpdateServiceForm, homeSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import JsonResponse
from django.template.loader import render_to_string
from consumer.models import Reviews
from django.db.models import Count

def privacyViews(request):
    return render(request, 'legal/privacypolicy.html')

def allsearch(request):
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    companies = Company.objects.all()
    form = SearchForm()
    Search = None
    results = []
    paginator = Paginator(companies, 6)
    page = request.GET.get('page')
    try:
        companiess = paginator.page(page)
    except PageNotAnInteger:
        companiess = paginator.page(1)
    except EmptyPage:
        companiess = paginator.page(paginator.num_pages)

    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            
            results = Company.objects.annotate(search=SearchVector('business_name','description'),).filter(search=Search)
            return render(request, 'business/company/list.html',{'page':page,'category':category, 'categories':categories ,'companies':results, 'name': Search,'form':form,'subcategories':subcategories})
    
    
    
    return render(request, 'business/home.html', {'page':page,'category':category, 'categories':categories, 'subcategories':subcategories,'form':form, 'companies':companiess})

def homesearch(request):
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    companies = Company.objects.all()
    form = homeSearchForm()
    Search = None
    results = []
    paginator = Paginator(companies, 6)
    page = request.GET.get('page')
    try:
        companiess = paginator.page(page)
    except PageNotAnInteger:
        companiess = paginator.page(1)
    except EmptyPage:
        companiess = paginator.page(paginator.num_pages)
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            results = Company.objects.annotate(search=SearchVector('business_name','description'),).filter(search=Search)
            return render(request, 'business/company/list.html',{'page':page,'category':category, 'categories':categories ,'companies':results, 'name': Search,'form':form})
    
    return render(request, 'business/home.html', {'page':page,'category':category, 'categories':categories, 'subcategories':subcategories,'form':form, 'companies':companiess})


# Create your views here.
def homepage(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    form = SearchForm()
    search = homeSearchForm()
    user = request.user
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'business/home.html', {'user':user,'search':search, 'category':category, 'categories':categories, 'subcategories':subcategories,'form':form})

def company_list(request, category_slug=None, company_slug=None, tag_slug=None):
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    companies = Company.objects.all()
    tag=None
    if category_slug:
        try:
            category = get_object_or_404(Category, slug=category_slug)
            companies = companies.filter(category=category)
            name = category.name
        except:
            subcategory = get_object_or_404(SubCategory, slug=category_slug)
            companies = companies.filter(subcategory=subcategory)
            name = subcategory.name
        
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        companies = companies.filter(tags__in=[tag])
    form = SearchForm()

    paginator = Paginator(companies, 6)
    page = request.GET.get('page')
    try:
        companiess = paginator.page(page)
    except PageNotAnInteger:
        companiess = paginator.page(1)
    except EmptyPage:
        companiess = paginator.page(paginator.num_pages)

    return render(request, 'business/company/list.html',{'page':page,'subcategories':subcategories,'category':category, 'companies':companiess, 'categories':categories, 'form':form,'tag':tag, 'name':name})

def company_detail(request, id, slug):
    company = get_object_or_404(Company, id=id, slug=slug, available=True)
    address = company.address
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    comp_categ = company.category
    services = Services.objects.all().filter(business=company)
    form = SearchForm()
    reviews = Reviews.objects.filter(company=company).order_by('-created')
    amenities = Amenities.objects.filter(company=company).order_by('amenity')
    sun_hour = OpeningHours.objects.get(company=company, weekday=0)
    mon_hour = OpeningHours.objects.get(company=company, weekday=1)
    tues_hour = OpeningHours.objects.get(company=company, weekday=2)
    wed_hour = OpeningHours.objects.get(company=company, weekday=3)
    thur_hour = OpeningHours.objects.get(company=company, weekday=4)
    fri_hour = OpeningHours.objects.get(company=company, weekday=5)
    sat_hour = OpeningHours.objects.get(company=company, weekday=6)
    galPhotos = Gallary.objects.filter(company=company)
    company_tags_ids = company.tags.values_list('id', flat=True)
    similar_companies = Company.objects.order_by().filter(tags__in=company_tags_ids).exclude(id=company.id).distinct()
    similar_companies = similar_companies.annotate(same_tags=Count('tags')).order_by('-same_tags', '-business_name').distinct()
    print(similar_companies.count())
    return render(request, 'business/company/detail.html', {'similar_companies':similar_companies,'photos':galPhotos,'sun_hour':sun_hour,'mon_hour':mon_hour,'tues_hour':tues_hour,'wed_hour':wed_hour,'thur_hour':thur_hour,'fri_hour':fri_hour,'sat_hour':sat_hour,'subcategories':subcategories,'comp_categ':comp_categ,'amenities':amenities,'address':address,'company':company,'category':category,'categories':categories, 'services':services, 'form':form, 'reviews':reviews})

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
            price_type = service_form.cleaned_data.get('price_type')
            price = service_form.cleaned_data.get('price')
            duration_hour = service_form.cleaned_data.get('duration_hour')
            duration_minute = service_form.cleaned_data.get('duration_minute')
            checkintime=service_form.cleaned_data.get('checkintime')
            padding=service_form.cleaned_data.get('padding')
            paddingtime_hour=service_form.cleaned_data.get('paddingtime_hour')
            paddingtime_minute=service_form.cleaned_data.get('paddingtime_minute')
            avail = True
            slugname = name + '' + request.user.slug
            service = Services.objects.create(business=company,name=name,description=description,price=price, available=avail, slug=slugname, 
                                                price_type=price_type,duration_hour=duration_hour,duration_minute=duration_minute,checkintime=checkintime,
                                                padding=padding,paddingtime_hour=paddingtime_hour,paddingtime_minute=paddingtime_minute)
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
    data = {'name': service.name, 'description': service.description, 'price_type':service.price_type, 'price':service.price, 'available':service.available, 'duration_hour':service.duration_hour, 'duration_minute':service.duration_minute}
    if request.method == 'POST':
        service_update_form = UpdateServiceForm(request.POST)
        if service_update_form.is_valid():
            name = service_update_form.cleaned_data.get('name')
            description = service_update_form.cleaned_data.get('description')
            price = service_update_form.cleaned_data.get('price')
            price_type= service_update_form.cleaned_data.get('price_type')
            duration_hour=service_update_form.cleaned_data.get('duration_hour')
            duration_minute=service_update_form.cleaned_data.get('duration_minute')
            checkintime=service_update_form.cleaned_data.get('checkintime')
            padding=service_update_form.cleaned_data.get('padding')
            paddingtime_hour=service_update_form.cleaned_data.get('paddingtime_hour')
            paddingtime_minute=service_update_form.cleaned_data.get('paddingtime_minute')
            serv = Services.objects.get(pk=pk)
            serv.name = name
            serv.description = description
            serv.price = price
            serv.price_type=price_type
            serv.duration_hour=duration_hour
            serv.duration_minute=duration_minute
            serv.checkintime=checkintime
            serv.padding=padding
            serv.paddingtime_hour=paddingtime_hour
            serv.paddingtime_minute=paddingtime_minute
            serv.save()
            return redirect(reverse('business:manage_service_list', args=[pks, slug]))
        else:
            context['service_update_form'] = service_update_form
    else:
        service_update_form = UpdateServiceForm(initial=data)
        context['service_update_form'] = service_update_form

    return render(request, 'business/company/manage/service/update.html',{'service':service, 'update_form':service_update_form})