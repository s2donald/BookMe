from django.shortcuts import render, get_object_or_404, redirect
from .forms import BusinessRegistrationForm, UpdateCompanyForm
from django.contrib.auth.decorators import login_required
from business.models import Company, SubCategory, OpeningHours, Services, Gallary, Amenities
from account.models import Account
from account.tasks import bizaddedEmailSent
from consumer.models import Bookings
from account.forms import AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django_hosts.resolvers import reverse
from django.http import JsonResponse
import json
from business.forms import AddCompanyForm, AddServiceForm, UpdateServiceForm, BookingSettingForm
from django.forms import inlineformset_factory
from django.views import View
from slugify import slugify

from .forms import MainPhoto

# Create your views here.
def businessadmin(request):
    user = request.user
    business = False
    if user.is_authenticated and user.is_business:
        business = True

    return render(request, 'welcome/welcome.html', {'business':business, 'none':'d-none'})

def pricingViews(request):
    user = request.user
    business = False
    if user.is_authenticated and user.is_business:
        business = True
    return render(request, 'welcome/pricing.html', {'business':business,'none':'d-none'})

def faqBusinessViews(request):
    user = request.user
    business = False
    if user.is_authenticated and user.is_business:
        business = True
    return render(request, 'welcome/faq.html', {'business':business,'none':'d-none'})

def completeViews(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    
    if user.on_board:
        return redirect(reverse('schedule', host='bizadmin')) 
    if request.method == 'POST':
        biz_form = AddCompanyForm(request.POST)
        booking_form = BookingSettingForm(request.POST)
        if biz_form.is_valid() and booking_form.is_valid():
            company = Company.objects.get(user=user)
            category = biz_form.cleaned_data.get('category')
            subcategory = biz_form.cleaned_data.get('subcategory')
            description = biz_form.cleaned_data.get('description')
            address = biz_form.cleaned_data.get('address')
            postal = biz_form.cleaned_data.get('postal')
            state = biz_form.cleaned_data.get('state')
            city = biz_form.cleaned_data.get('city')
            interval = booking_form.cleaned_data.get('interval')
            notes = booking_form.cleaned_data.get('notes')
            cancellation = booking_form.cleaned_data.get('cancellation')
            subdomain = request.POST.get('subdomain',company.slug)
            returning = request.POST.get('returning', False)
            sun_from = request.POST['sunOpenHour']
            sun_to = request.POST['sunCloseHour']
            sun_closed = not request.POST.get('sunOpen', False)
            mon_from = request.POST['monOpenHour']
            mon_to = request.POST['monCloseHour']
            mon_closed = not request.POST.get('monOpen', False)
            tues_from = request.POST['tuesCloseHour']
            tues_to = request.POST['tuesOpenHour']
            tues_closed = not request.POST.get('tuesOpen', False)
            wed_from = request.POST['wedOpenHour']
            wed_to = request.POST['wedCloseHour']
            wed_closed = not request.POST.get('wedOpen', False)
            thurs_from = request.POST['thursOpenHour']
            thurs_to = request.POST['thursCloseHour']
            thurs_closed = not request.POST.get('thursOpen', False)
            fri_from = request.POST['friOpenHour']
            fri_to = request.POST['friCloseHour']
            fri_closed = not request.POST.get('friOpen', False)
            sat_from = request.POST['satOpenHour']
            sat_to = request.POST['satCloseHour']
            sat_closed = not request.POST.get('satOpen', False)

            status = 'published'
            company.category = category
            company.description = description
            company.address = address
            company.postal = postal
            company.state = state
            company.city = city
            company.status = status
            company.interval = interval
            company.returning = returning
            company.notes = notes
            company.cancellation = cancellation
            if subdomain != company.slug:
                company.slug = slugify(subdomain)
            company.save()
            user.on_board = True
            user.save()
            objs = [
                OpeningHours.objects.get(company=company, weekday=0),
                OpeningHours.objects.get(company=company, weekday=1),
                OpeningHours.objects.get(company=company, weekday=2),
                OpeningHours.objects.get(company=company, weekday=3),
                OpeningHours.objects.get(company=company, weekday=4),
                OpeningHours.objects.get(company=company, weekday=5),
                OpeningHours.objects.get(company=company, weekday=6),
            ]
            objs[0].is_closed = sun_closed
            objs[1].is_closed = mon_closed
            objs[2].is_closed = tues_closed
            objs[3].is_closed = wed_closed
            objs[4].is_closed = thurs_closed
            objs[5].is_closed = fri_closed
            objs[6].is_closed = sat_closed

            objs[0].from_hour = sun_from
            objs[1].from_hour = mon_from
            objs[2].from_hour = tues_from
            objs[3].from_hour = wed_from
            objs[4].from_hour = thurs_from
            objs[5].from_hour = fri_from
            objs[6].from_hour = sat_from

            objs[0].to_hour = sun_to
            objs[1].to_hour = mon_to
            objs[2].to_hour = tues_to
            objs[3].to_hour = wed_to
            objs[4].to_hour = thurs_to
            objs[5].to_hour = fri_to
            objs[6].to_hour = sat_to

            OpeningHours.objects.bulk_update(objs,['is_closed','from_hour','to_hour'])
            for s in subcategory:
                company.subcategory.add(s)

            return render(request, 'bizadmin/home/home.html', {'company':company})

    biz_form = AddCompanyForm()
    service_form = AddServiceForm()
    booking_form = BookingSettingForm()
    subcategories = SubCategory.objects.all()
    company = Company.objects.get(user=user)
    services = Services.objects.filter(business=company)
    sunday = OpeningHours.objects.get(company=company, weekday=0)
    monday = OpeningHours.objects.get(company=company, weekday=1)
    tuesday = OpeningHours.objects.get(company=company, weekday=2)
    wednesday = OpeningHours.objects.get(company=company, weekday=3)
    thursday = OpeningHours.objects.get(company=company, weekday=4)
    friday = OpeningHours.objects.get(company=company, weekday=5)
    saturday = OpeningHours.objects.get(company=company, weekday=6)

    return render(request, 'bizadmin/dashboard/profile/addcompany.html', {'booking_form':booking_form,'sunday':sunday,'monday':monday,'tuesday':tuesday,'wednesday':wednesday,'thursday':thursday,'friday':friday,'saturday':saturday,
                                                                                'biz_form':biz_form, 'service_form':service_form,'subcategories':subcategories,'company':company,
                                                                                'services':services})

class subdomainCheck(View):
    def post(self, request):
        data=json.loads(request.body)
        subdomain = data['subdomain']
        company = Company.objects.get(user=request.user)
        if not subdomain:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        if (company.slug!=str(subdomain)) and (Company.objects.filter(slug=subdomain).exists()):
            return JsonResponse({'email_error':'This subdomain already exists! Please try another.','email_valid':True})

        if subdomain != slugify(subdomain):
            return JsonResponse({'email_error':'Subdomains must only contain lowercase letters, numbers and hyphens.','email_valid':True})
        return JsonResponse({'email_valid':False})

def signupViews(request):
    context = {}
    if request.method == 'POST':
        user_form = BusinessRegistrationForm(request.POST)
        
        if user_form.is_valid():
            user_form.save()
            email = user_form.cleaned_data.get('email')
            raw_pass = user_form.cleaned_data.get('password1')
            bname = request.POST.get('bname', '')
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            company = Company.objects.create(user=account,business_name=bname,
                                                description='',address='',postal='',
                                                state='',city='',status='draft', avgrating=0)
            biz_hours = OpeningHours.objects.bulk_create([
                OpeningHours(company=company, weekday=0,is_closed=True),
                OpeningHours(company=company, weekday=1,is_closed=False),
                OpeningHours(company=company, weekday=2,is_closed=False),
                OpeningHours(company=company, weekday=3,is_closed=False),
                OpeningHours(company=company, weekday=4,is_closed=False),
                OpeningHours(company=company, weekday=5,is_closed=False),
                OpeningHours(company=company, weekday=6,is_closed=True),
            ])
            return redirect(reverse('completeprofile', host='bizadmin'))
        else:
            context['business_registration_form'] = user_form
            
    else:
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
    return render(request, 'account/bussignup.html', {'user_form':user_form, 'none':'d-none'})

def loginViews(request):
    context = {}
    if request.method == 'POST':
        user_form = AccountAuthenticationForm(request.POST)
        if user_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            account = authenticate(email=email, password=password)
            if account:
                login(request, account)
                if account.is_business:
                    if account.on_board:
                        return redirect(reverse('home', host='bizadmin'))
                    else:
                        return redirect(reverse('completeprofile', host='bizadmin'))
                        
                else:
                    return redirect(reverse('notbusiness', host='bizadmin'))
        else:
            context['business_registration_form'] = user_form
            
    else:
        user_form = AccountAuthenticationForm()
        context['business_registration_form'] = user_form
    return render(request, 'account/buslogin.html', {'user_form':user_form, 'none':'d-none'})

def profileViews(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            image_form = MainPhoto()
            return render(request, 'bizadmin/dashboard/account/profile.html',{'company':company, 'image_form':image_form})
        else:
            return redirect(reverse('completeprofile', host='bizadmin'))
    else:
        loginViews(request)
    

def profileBillingViews(request):
    return render(request,'bizadmin/dashboard/account/billing.html')

def profileSecurityViews(request):
    return render(request,'bizadmin/dashboard/account/security.html')

@login_required
def scheduleView(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            bookings = Bookings.objects.filter(company=company)
            return render(request, 'bizadmin/dashboard/schedule.html', {'company':company, 'bookings':bookings})
        else:
            return redirect(reverse('completeprofile', host='bizadmin'))
    else:
        loginViews(request)

def fileUploadView(request):
    if request.POST:
        return JsonResponse({'works':'works'})

def LogoutView(request):
    logout(request)
    return render(request, 'welcome/welcome.html', {'business':False})

from django.template.loader import render_to_string
def save_service_form(request, form, template_name):
    data=dict()
    if request.method=='POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            price_type = form.cleaned_data.get('price_type')
            price = form.cleaned_data.get('price')
            duration_hour = form.cleaned_data.get('duration_hour')
            duration_minute = form.cleaned_data.get('duration_minute')
            checkintime=form.cleaned_data.get('checkintime')
            padding=form.cleaned_data.get('padding')
            paddingtime_hour=form.cleaned_data.get('paddingtime_hour')
            paddingtime_minute=form.cleaned_data.get('paddingtime_minute')
            avail = True
            company = Company.objects.get(user=request.user)
            service = Services.objects.create(business=company,name=name,description=description,price=price, available=avail, 
                                                price_type=price_type,duration_hour=duration_hour,duration_minute=duration_minute,checkintime=checkintime,
                                                padding=padding,paddingtime_hour=paddingtime_hour,paddingtime_minute=paddingtime_minute)
            service.save()
            data['form_is_valid'] = True
            services = Services.objects.filter(business=company)
            data['html_service_list'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_list.html', {'services':services})
            data['view'] = 'Your service has been created!'
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
    
    context = {'service_form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

#used in the onboarding page
def createserviceViews(request):
    if request.method=='POST':
        service_form = AddServiceForm(request.POST)
    else:
        service_form = AddServiceForm()
    return save_service_form(request, service_form, 'bizadmin/dashboard/profile/services/partial_service_create.html')

#used in the bizadmin page
class createserviceAPI(View):
    def post(self,request):
        form = AddServiceForm(request.POST)
        data = dict()
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_type = form.cleaned_data.get('price_type')
            price = form.cleaned_data.get('price')
            duration_hour = form.cleaned_data.get('duration_hour')
            duration_minute = form.cleaned_data.get('duration_minute')
            checkintime=form.cleaned_data.get('checkintime')
            padding=form.cleaned_data.get('padding')
            paddingtime_hour=form.cleaned_data.get('paddingtime_hour')
            paddingtime_minute=form.cleaned_data.get('paddingtime_minute')
            avail = True
            company = Company.objects.get(user=request.user)
            service = Services.objects.create(business=company,name=name,description=description,price=price, available=avail, 
                                                price_type=price_type,duration_hour=duration_hour,duration_minute=duration_minute,checkintime=checkintime,
                                                padding=padding,paddingtime_hour=paddingtime_hour,paddingtime_minute=paddingtime_minute)
            service.save()
            data['form_is_valid'] = True
            data['view'] = 'Your service has been created!'
            data['icon'] = 'success'
        else:
            data['form_is_valid'] = False
            data['view'] = 'Your service was not created. There was an error.'
            data['icon'] = 'error'
        company = Company.objects.get(user=request.user)
        services = Services.objects.filter(business=company)
        data['html_service_list'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_list.html', {'services':services})
        return JsonResponse(data)





#used in the onboarding page
def deleteserviceViews(request, pk):

    company = Company.objects.get(user=request.user)
    service = get_object_or_404(Services, pk=pk, business=company)
    data = dict()
    if request.method=='POST':
        service.delete()
        data['form_is_valid']=True
        services = Services.objects.filter(business=company)
        data['html_service_list'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_list.html', {'services':services})
        data['view'] = 'Your service has been deleted'
    else:
        context = {'service':service}
        data['html_form'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_delete.html', context, request=request)
    return JsonResponse(data)

#used in the bizadmin page
class deleteserviceAPI(View):
    
    def post(self, request):
        data = dict()
        dataa = json.loads(request.body)
        s_id=dataa['serv_id']
        company = Company.objects.get(user=request.user)
        service = get_object_or_404(Services, pk=s_id, business=company)
        service.delete()
        services = Services.objects.filter(business=company)
        data['html_service_list'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_list.html', {'services':services})
        return JsonResponse(data)

#used in the onboarding page
def updateserviceViews(request, pk):
    service = get_object_or_404(Services, pk=pk)
    company = Company.objects.get(user=request.user)
    dat = {'name': service.name, 'description': service.description, 'price_type':service.price_type, 'price':service.price, 'available':service.available, 'duration_hour':service.duration_hour, 'duration_minute':service.duration_minute, 'checkintime':service.checkintime, 'padding':service.padding, 'paddingtime_hour':service.paddingtime_hour, 'paddingtime_minute':service.paddingtime_minute}
    data=dict()
    if request.method=='POST':
        form = UpdateServiceForm(request.POST)
        if form.is_valid():
            
            service.name = form.cleaned_data.get('name')
            service.description = form.cleaned_data.get('description')
            service.price_type = form.cleaned_data.get('price_type')
            service.price = form.cleaned_data.get('price')
            service.duration_hour = form.cleaned_data.get('duration_hour')
            service.duration_minute = form.cleaned_data.get('duration_minute')
            service.checkintime = form.cleaned_data.get('checkintime')
            service.padding = form.cleaned_data.get('padding')
            service.paddingtime_hour = form.cleaned_data.get('paddingtime_hour')
            service.paddingtime_minute = form.cleaned_data.get('paddingtime_minute')
            service.avail = True
            company = Company.objects.get(user=request.user)
            service.save()
            data['form_is_valid'] = True
            services = Services.objects.filter(business=company)
            data['html_service_list'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_list.html', {'services':services})
            data['view'] = 'Your service has been updated'
        else:
            data['form_is_valid'] = False
        return JsonResponse(data)
    else:
        form = UpdateServiceForm(initial=dat)
    context = {'service_form':form, 'service':service}
    data['html_form'] = render_to_string('bizadmin/dashboard/profile/services/partial_service_update.html', context, request=request)
    return JsonResponse(data)



## Adding the homepage views and all stuff required for the homepage
from django.utils import timezone
import pytz
from datetime import timedelta
from django.db.models import Sum
from decimal import Decimal
@login_required
def homepageViews(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            bpp = 0
            if company.image:
                bpp = bpp + 25
            gallary = Gallary.objects.filter(company=company)
            if gallary:
                count = gallary.count()
                if count==1:
                    bpp = bpp +25
                elif count == 2:
                    bpp = bpp +50
                else:
                    bpp =100
                
            week = timezone.now() - timedelta(days=7)
            twoweek = week - timedelta(days=7)
            threeweek = twoweek - timedelta(days=7)
            fourweek = threeweek - timedelta(days=7)
            week1 = Bookings.objects.filter(company=company, end__gte=week, end__lte=timezone.now()).aggregate(Sum('price')).get('price__sum',0)
            if not week1:
                week1 = 0
            start1 = (week - timedelta(days=week.weekday())).strftime("%b-%d-%Y")
            
            week2 = Bookings.objects.filter(company=company, end__gte=twoweek, end__lte=week).aggregate(Sum('price')).get('price__sum',0)
            if not week2:
                week2 = 0
            start2 = (twoweek - timedelta(days=twoweek.weekday())).strftime("%b-%d-%Y")

            week3 = Bookings.objects.filter(company=company, end__gte=threeweek, end__lte=twoweek).aggregate(Sum('price')).get('price__sum',0)
            if not week3:
                week3 = 0
            start3 = (threeweek - timedelta(days=threeweek.weekday())).strftime("%b-%d-%Y")

            week4 = Bookings.objects.filter(company=company, end__gte=fourweek, end__lte=threeweek).aggregate(Sum('price')).get('price__sum',0)
            if not week4:
                week4 = 0
            start4 = (fourweek - timedelta(days=fourweek.weekday())).strftime("%b-%d-%Y")
            week = [int(week4), int(week3), int(week2), int(week1)]
            weeklabel = [start4, start3, start2, start1]

            month = timezone.now() - timedelta(days=30)
            month1 = Bookings.objects.filter(company=company, end__gte=month, end__lte=timezone.now()).aggregate(Sum('price')).get('price__sum',0)
            if not month1:
                month1 = 0
            labelM0 = timezone.now().strftime("%b-%Y")
            labelM1 = month.strftime("%b-%Y")

            twomonth = month - timedelta(days=30)
            month2 = Bookings.objects.filter(company=company, end__gte=twomonth, end__lte=month).aggregate(Sum('price')).get('price__sum',0)
            if not month2:
                month2 = 0
            labelM2 = twomonth.strftime("%b-%Y")

            threemonth = twomonth - timedelta(days=30)
            month3 = Bookings.objects.filter(company=company, end__gte=threemonth, end__lte=twomonth).aggregate(Sum('price')).get('price__sum',0)
            if not month3:
                month3 = 0
            labelM3 = threemonth.strftime("%b-%Y")

            fourmonth = threemonth - timedelta(days=30)
            month4 = Bookings.objects.filter(company=company, end__gte=fourmonth, end__lte=threemonth).aggregate(Sum('price')).get('price__sum',0)
            if not month4:
                month4 = 0
            labelM4 = fourmonth.strftime("%b-%Y")

            fivemonth = fourmonth - timedelta(days=30)
            month5 = Bookings.objects.filter(company=company, end__gte=fivemonth, end__lte=fourmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month5:
                month5 = 0
            labelM5 = fivemonth.strftime("%b-%Y")

            sixmonth = fivemonth - timedelta(days=30)
            month6 = Bookings.objects.filter(company=company, end__gte=sixmonth, end__lte=fivemonth).aggregate(Sum('price')).get('price__sum',0)
            if not month6:
                month6 = 0
            labelM6 = sixmonth.strftime("%b-%Y")

            sevenmonth = sixmonth - timedelta(days=30)
            month7 = Bookings.objects.filter(company=company, end__gte=sevenmonth, end__lte=sixmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month7:
                month7 = 0
            labelM7 = sevenmonth.strftime("%b-%Y")

            eightmonth = sevenmonth - timedelta(days=30)
            month8 = Bookings.objects.filter(company=company, end__gte=eightmonth, end__lte=sevenmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month8:
                month8 = 0
            labelM8 = eightmonth.strftime("%b-%Y")

            ninemonth = eightmonth - timedelta(days=30)
            month9 = Bookings.objects.filter(company=company, end__gte=ninemonth, end__lte=eightmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month9:
                month9 = 0
            labelM9 = ninemonth.strftime("%b-%Y")

            tenmonth = ninemonth - timedelta(days=30)
            month10 = Bookings.objects.filter(company=company, end__gte=tenmonth, end__lte=ninemonth).aggregate(Sum('price')).get('price__sum',0)
            if not month10:
                month10 = 0
            labelM10 = tenmonth.strftime("%b-%Y")

            elevenmonth = tenmonth - timedelta(days=30)
            month11 = Bookings.objects.filter(company=company, end__gte=elevenmonth, end__lte=tenmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month11:
                month11 = 0
            labelM11 = elevenmonth.strftime("%b-%Y")

            twelvemonth = elevenmonth - timedelta(days=30)
            month12 = Bookings.objects.filter(company=company, end__gte=twelvemonth, end__lte=elevenmonth).aggregate(Sum('price')).get('price__sum',0)
            if not month12:
                month12 = 0
            labelM12 = twelvemonth.strftime("%b-%Y")

            month = [int(month12),int(month11),int(month10),int(month9),int(month8),int(month7),int(month6),int(month5),int(month4),int(month3),int(month2),int(month1),]
            monthlabel = [labelM11,labelM10,labelM9,labelM8,labelM7,labelM6,labelM5,labelM4,labelM3,labelM2,labelM1,labelM0]
            return render(request,'bizadmin/home/home.html', {'company':company, 'week':week, 'weeklabel':weeklabel, 'month':month, 'monthlabel':monthlabel, 'bpp':bpp})
        else:
            return redirect(reverse('completeprofile', host='bizadmin'))
    else:
        loginViews(request)

from PIL import Image
from django.core.files import File
from io import BytesIO
from django.core.files.base import ContentFile

#For the main image on the company info
@login_required
def headerImageUpload(request):
    if request.POST:
        company = Company.objects.get(user=request.user)
        img = request.FILES.get('imageFile')
        x = Decimal(request.POST.get('x'))
        y = Decimal(request.POST.get('y'))
        w = Decimal(request.POST.get('width'))
        h = Decimal(request.POST.get('height'))
        if img:
            image = Image.open(img)
            box = (x, y, w+x, h+y)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((500,500),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image.format)
            company.image.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            company.save()
    
    return redirect(reverse('information', host='bizadmin'))

#For the gallery and photos main photo
@login_required
def headerImageUploads(request):
    if request.POST:
        company = Company.objects.get(user=request.user)
        img = request.FILES.get('imageFile')
        x = Decimal(request.POST.get('x'))
        y = Decimal(request.POST.get('y'))
        w = Decimal(request.POST.get('width'))
        h = Decimal(request.POST.get('height'))
        if img:
            image = Image.open(img)
            box = (x, y, w+x, h+y)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((500,500),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image.format)
            company.image.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            company.save()
    
    return redirect(reverse('photos', host='bizadmin'))
        
def galImageUpload(request):
    if request.POST:
        company = Company.objects.get(user=request.user)
        img = request.FILES.get('gallaryFile')
        x = Decimal(request.POST.get('xs'))
        y = Decimal(request.POST.get('ys'))
        w = Decimal(request.POST.get('widths'))
        h = Decimal(request.POST.get('heights'))
        if img:
            image = Image.open(img)
            box = (x, y, w+x, h+y)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((500,500),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image.format)
            gallary = Gallary.objects.create(company=company)
            gallary.photos.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            gallary.save()
    
    return redirect(reverse('photos', host='bizadmin'))

##Business Page Views
@login_required
def businessPhotoView(request):
    company = Company.objects.get(user=request.user)
    photos = Gallary.objects.filter(company=company)
    return render(request,'bizadmin/businesspage/photos.html',{'company':company, 'photos':photos})

def businessAmenitiesView(request):
    company = Company.objects.get(user=request.user)
    amenities = Amenities.objects.filter(company=company)

    return render(request,'bizadmin/businesspage/amenities.html',{'company':company, 'amenities':amenities})

class addTagAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['addedTag']
        company = Company.objects.get(user=request.user)
        company.tags.add(tag)
        if not tag:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        return JsonResponse({'tags':'works'})

class removeTagAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['removedTag']
        company = Company.objects.get(user=request.user)
        company.tags.remove(tag)
        if not tag:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        return JsonResponse({'tags':'works'})

import string
class addAmenityAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['addedAmenity']
        tag = string.capwords(tag)
        company = Company.objects.get(user=request.user)
        Amenities.objects.create(amenity=tag, company=company)
        if not tag:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        return JsonResponse({'tags':'works'})

class removeAmenityAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['removedAmenity']
        company = Company.objects.get(user=request.user)
        amen = Amenities.objects.get(amenity=tag, company=company)
        amen.delete()

        if not tag:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        return JsonResponse({'tags':'works'})

class deleteGalPic(View):
    def post(self, request):
        data = json.loads(request.body)
        pic_id = data['pics_id']
        company = Company.objects.get(user=request.user)
        picture = Gallary.objects.get(company=company, id=pic_id)
        picture.delete()

        return JsonResponse({'pictures':'pictures'})

def compinfoViews(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    
    if not user.on_board:
        return redirect(reverse('completeprofile', host='bizadmin'))

    company = Company.objects.get(user=user)
    subcategory = company.subcategory.all()
    s = [x.id for x in subcategory]
    initialVal = {'business_name':company.business_name,'email':company.email,'category':company.category, 'description':company.description,
                    'subcategory':s, 'address':company.address, 'postal':company.postal, 'city':company.city, 'state':company.state,
                    'fb_link':company.fb_link,'twitter_link':company.twitter_link,'instagram_link':company.instagram_link,'website_link':company.website_link,'phone':company.phone}
    updateform = UpdateCompanyForm(initial=initialVal)
    return render(request, 'bizadmin/companydetail/info/compinfo.html', {'company':company, 'updateform': updateform})

#This update form updates the company detail info
class updateCompanyDetail(View):
    def post(self, request):
        data = json.loads(request.body)
        bname = data['name']
        email = data['email']
        if not bname:
            return JsonResponse({'name_error':'You must include a business name'})
        if (request.user.email!=str(email)) and (Account.objects.filter(email=email).exists()):
            return JsonResponse({'email_error':'This email already exists!'})
        return JsonResponse({'good':'we good'})

class saveCompanyDetail(View):
    def post(self, request):
        form = UpdateCompanyForm(request.POST)
        context = {}
        if form.is_valid():
            company = Company.objects.get(user=request.user)
            company.business_name = form.cleaned_data.get('business_name')
            company.category = form.cleaned_data.get('category')
            subcategory = form.cleaned_data.get('subcategory')
            print(subcategory)
            email = form.cleaned_data.get('email')
            if not email==company.email:
                company.email = email
            phone = form.cleaned_data.get('phone')
            if not phone == company.phone:
                company.phone = phone
            company.description = form.cleaned_data.get('description')
            company.address = form.cleaned_data.get('address')
            company.postal = form.cleaned_data.get('postal')
            company.city = form.cleaned_data.get('city')
            company.province = form.cleaned_data.get('province')
            company.website_link = form.cleaned_data.get('website_link')
            company.fb_link = form.cleaned_data.get('fb_link')
            company.twitter_link = form.cleaned_data.get('twitter_link')
            company.instagram_link = form.cleaned_data.get('instagram_link')
            company.save()
            subcat = company.subcategory.all()
            for s in subcat:
                company.subcategory.remove(s)
            for s in subcategory:
                company.subcategory.add(s)
            return JsonResponse({'good':'We have saved your company information!'})
        else:
            return JsonResponse({'errors':'Please double check your form. There may be errors.'})

def servicesDetailView(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        context['business_registration_form'] = user_form
        return render(request, 'account/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if not user.on_board:
        return redirect(reverse('completeprofile', host='bizadmin'))

    company = Company.objects.get(user=user)
    services = Services.objects.filter(business=company)
    service_form = AddServiceForm()
    return render(request,'bizadmin/companydetail/services/service.html', {'company':company, 'services':services, 'service_form':service_form})





    