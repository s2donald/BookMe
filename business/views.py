from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Company, Services, SubCategory, Amenities, OpeningHours, Gallary
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import SearchForm, AddServiceForm, UpdateServiceForm, homeSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import JsonResponse
from django.template.loader import render_to_string
from consumer.models import Reviews, Bookings
from django.db.models import Count
from django.db.models import F
import json, geocoder
from django.views import View
from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.db.models.functions import Distance, GeometryDistance
from django.contrib.postgres.search import TrigramSimilarity

def privacyViews(request):
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    form = SearchForm()
    search = homeSearchForm()
    user = request.user
    return render(request, 'legal/privacypolicy.html', {'user':user,'search':search, 'category':category, 'categories':categories, 'subcategories':subcategories,'form':form})

def tosViews(request):
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    form = SearchForm()
    search = homeSearchForm()
    user = request.user
    return render(request, 'legal/termsofservice.html', {'user':user,'search':search, 'category':category, 'categories':categories, 'subcategories':subcategories,'form':form})

def allsearch(request):
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    companies = Company.objects.all()
    form = SearchForm()
    Search = None
    cat = None
    subcat = None
    q = 0
    loc = None
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if 'Location' in request.GET:
            q = 1
            form = homeSearchForm(request.GET)
            categorys = request.GET['category']
            if categorys:
                try:
                    cat = Category.objects.get(pk=categorys)
                except:
                    subcat = SubCategory.objects.get(pk=categorys)

        if form.is_valid():
            Search = form.cleaned_data['Search']

            if q == 1:
                loc = form.cleaned_data['Location']
            
            if not loc:
                if not request.user.is_authenticated:
                    loc = 'me'
                elif request.user.address:
                    loc = request.user.address
                else:
                    loc = 'me'
            # results = Company.objects.annotate(search=SearchVector('business_name','description'),).filter(search=Search)
            #This may need to ge optimized
            results = Services.objects.annotate(similarity=TrigramSimilarity('name', Search),).filter(similarity__gt=0.1).order_by('-similarity')
            ids = results.values_list('business', flat=True).distinct()
            searchvector = SearchVector('business_name', weight='A') + SearchVector('description', weight='B')
            searchquery = SearchQuery(Search)
            
            results = Company.objects.filter(id__in=ids)|Company.objects.annotate(similarity=TrigramSimilarity('business_name', Search),).filter(similarity__gt=0.1).order_by('-similarity')
            
            
            results = results.filter(status='published')

            if loc=='me':
                ip = geocoder.ipinfo('me').latlng
            else:
                ip = geocoder.google(loc, key="AIzaSyBaZM_O3d1-xDrecS_fbcbvoT5qDmLmje0").latlng
            
            if ip:
                lat = ip[0]
                lng = ip[1]
                pnt = Point(lng,lat, srid=4326)
                results = results.annotate(distance=GeometryDistance("location", pnt)).order_by("distance")
            else:
                if cat:
                    results = results.filter(category=cat).order_by('business_name')
                if subcat:
                    results = results.filter(subcategory=subcat).order_by('business_name')
                if not cat and not subcat:    
                    results = results.order_by('business_name')

            total = results.count()
            paginator = Paginator(results, 6)
            page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            return render(request, 'business/company/list.html',{'total':total,'page':page,'category':category, 'categories':categories ,'companies':results, 'name': Search,'form':form,'subcategories':subcategories})
    return render(request, 'business/company/list.html')

# Create your views here.
def homepage(request):
    categories = Category.objects.all().exclude(slug="other")
    otherObj = Category.objects.get(slug="other")
    subcategories = SubCategory.objects.all()
    search = homeSearchForm()
    user = request.user
    return render(request, 'business/home.html', {'otherObj':otherObj,'user':user,'search':search, 'categories':categories, 'subcategories':subcategories})

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
    companies = companies.filter(status='published')
    ip = geocoder.ipinfo('me').latlng
    if ip:
        lat = ip[0]
        lng = ip[1]
        pnt = GEOSGeometry('POINT('+ str(lng) + ' ' + str(lat) + ')', srid=4326)
        companies = companies.annotate(distance=Distance('location', pnt)).order_by('distance')
    total = companies.count()
    paginator = Paginator(companies, 6)
    page = request.GET.get('page')
    try:
        companiess = paginator.page(page)
    except PageNotAnInteger:
        companiess = paginator.page(1)
    except EmptyPage:
        companiess = paginator.page(paginator.num_pages)
    return render(request, 'business/company/list.html',{'total':total,'page':page,'subcategories':subcategories,'category':category, 'companies':companiess, 'categories':categories, 'form':form,'tag':tag, 'name':name})

def company_detail(request, id, slug):
    company = get_object_or_404(Company, id=id, slug=slug, available=True)
    address = company.address
    category = None
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
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
    similar_companies = similar_companies.annotate(same_tags=Count('tags')).order_by('-same_tags', '-business_name').distinct()[:10]
    paginator = Paginator(reviews, 6)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)


    return render(request, 'business/company/detail.html', {'page':page,'similar_companies':similar_companies,'photos':galPhotos,'sun_hour':sun_hour,'mon_hour':mon_hour,'tues_hour':tues_hour,'wed_hour':wed_hour,'thur_hour':thur_hour,'fri_hour':fri_hour,'sat_hour':sat_hour,'subcategories':subcategories,'amenities':amenities,'address':address,'company':company,'category':category,'categories':categories, 'services':services, 'form':form, 'reviews':reviews})

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

from django.template.loader import render_to_string
class company_like(View):
    def post(self, request):
        if not request.user.is_authenticated:
            data = {}
            data['good'] = False
            return JsonResponse(data)
        data=json.loads(request.body)
        ids = data['company_id']
        action = data['action']
        company = Company.objects.get(pk=ids)
        if action == 'like':
            company.users_like.add(request.user)
            data['hearts'] = render_to_string('business/company/user_like/like.html', {'company':company})
        else:
            company.users_like.remove(request.user)
            data['hearts'] = render_to_string('business/company/user_like/unlike.html', {'company':company})
        data['good'] = True
        return JsonResponse(data)
    
class cancelAppointmentAjax(View):
    def post(self, request):
        booking_id = request.POST.get('booking_id')
        bookings = Bookings.objects.get(pk=booking_id)
        if request.user == bookings.user:
            bookings.is_cancelled_user = True
            bookings.save()
            #We need to send an email to the company saying the client cancelled the appointment
        return JsonResponse({'':''})

def getCompanyName(request):
    name = ''
    if request.GET:
        company = Company.objects.get(id=request.GET.get('company_id'))
        name = company.business_name
    return JsonResponse({'companyname':name})

def addReviewView(request):
    if request.POST:
        if request.user.is_authenticated:
            company = Company.objects.get(id=request.POST.get('company_id'))
            review = request.POST.get('wordReview')
            star = request.POST.get('starReview')
            reviews = Reviews.objects.create(company=company, reviewer=request.user, review=review, star=star)
            reviews.save()
            #now send the email to the user
    return JsonResponse({'savedReview':True})
