from django.shortcuts import render, get_object_or_404, redirect
from businessadmin.forms import formBuilderForm, StaffMemberForms, BusinessRegistrationForm, AddHoursForm, UpdateCompanyForm, AddClientForm, AddNotesForm, CreateSmallBizForm, AddBookingForm, BusinessName, AddServiceCategoryForm, AddServiceToCategory
from django.contrib.auth.decorators import login_required
from django import forms
from businessadmin.models import StaffMember, Breaks, StaffWorkingHours
from business.models import Company, SubCategory, OpeningHours, Services, Gallary, Amenities, Clients, CompanyReq, ServiceCategories
from account.models import Account
from calendarapp.models import formBuilder, bookingForm
from account.forms import UpdatePersonalForm
from products.tasks import bizCreatedEmailSent
from consumer.models import Bookings, Reviews, extraInformation
from account.forms import AccountAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django_hosts.resolvers import reverse
from django.http import JsonResponse
import json
from django.http.response import HttpResponse
from business.forms import AddServiceForm, UpdateServiceForm, BookingSettingForm
from .forms import AddCompanyForm, AddProductForm, questionProductForm
from django.forms import inlineformset_factory
from products.models import Product as ProductModel
from products.models import MainProductDropDown, ProductDropDown, QuestionModels, Order, OrderItem
from django.views import View
from slugify import slugify
from businessadmin.forms import MainPhoto, ServicePaymentCollectForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from businessadmin.tasks import addedOnCompanyList, requestToBeClient, appointmentCancelled
from account.tasks import reminderEmail, confirmedEmail, consumerCreatedEmailSent, send_sms_confirmed_client, send_sms_reminder_client, declinedRequestEmail, send_sms_declined_request_client
import re
from django.db import transaction
import urllib
from django.conf import settings
import requests
import djstripe
from .forms import dropDownForm, dropDownOptionsForm
# Create your views here.
def businessadmin(request):
    user = request.user
    return render(request, 'welcomes/welcome.html', {'user':user, 'none':'d-none'})

def termsViews(request):
    user = request.user
    return render(request, 'welcomes/terms/terms.html', {'user':user, 'none':'d-none'})

def privacyViews(request):
    user = request.user
    return render(request, 'welcomes/terms/privacy.html', {'user':user, 'none':'d-none'})

def pricingViews(request):
    user = request.user
    return render(request, 'welcomes/pricing.html', {'user':user,'none':'d-none'})

def faqBusinessViews(request):
    user = request.user
    return render(request, 'welcomes/faq.html', {'user':user,'none':'d-none'})

def createNewStaff(company_id, user_id, first_name, last_name, phone, email, slug, login, access):
    company = Company.objects.get(pk=company_id)
    if user_id:
        acct = Account.objects.get(user_id)
    return 'helo'
    

def createNewBusiness(request):
    user = request.user
    user_form = CreateSmallBizForm()
    if not user.is_authenticated:
        user_form = AccountAuthenticationForm()
        context['business_registration_form'] = user_form
        return render(request, 'accountprod/buslogin.html', {'user_form':user_form, 'none':'d-none'})

    if request.method == 'POST':
        user_form = CreateSmallBizForm(request.POST)
        
        if user_form.is_valid():
            email = user_form.cleaned_data.get('email')
            phone = user_form.cleaned_data.get('phone')
            bname = user_form.cleaned_data.get('business_name')
            company = Company.objects.create(user=user,business_name=bname,email=email,phone=phone,
                                                description='',address='',postal='',
                                                state='',city='',status='draft')
            company.save()
            biz_hours = OpeningHours.objects.bulk_create([
                OpeningHours(company=company, weekday=0,is_closed=True),
                OpeningHours(company=company, weekday=1,is_closed=False),
                OpeningHours(company=company, weekday=2,is_closed=False),
                OpeningHours(company=company, weekday=3,is_closed=False),
                OpeningHours(company=company, weekday=4,is_closed=False),
                OpeningHours(company=company, weekday=5,is_closed=False),
                OpeningHours(company=company, weekday=6,is_closed=True),
            ])
            user.is_business=True
            user.save()
            return redirect(reverse('completeprofile', host='prodadmin'))
        else:
            context['business_registration_form'] = user_form

    if user.on_board:
        return redirect(reverse('home', host='prodadmin'))
    
    
    return render(request, 'accountprod/createbusiness.html', {'user':user, 'none':'d-none', 'user_form':user_form})
@login_required
def completeViews(request):
    if not request.user.is_authenticated:
        user_form = AccountAuthenticationForm()
        context['business_registration_form'] = user_form
        return render(request, 'accountprod/buslogin.html', {'user_form':user_form, 'none':'d-none'})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    biz_form = AddCompanyForm()
    product_form = AddProductForm()
    company = Company.objects.get(user=user)
    booking_form = BookingSettingForm()
    addon_form = dropDownForm()
    if user.on_board:
        return redirect(reverse('home', host='prodadmin')) 
    if request.method == 'POST':
        biz_form = AddCompanyForm(request.POST)
        booking_form = BookingSettingForm(request.POST)
        if biz_form.is_valid() and booking_form.is_valid():
            description = biz_form.cleaned_data.get('description')
            address = biz_form.cleaned_data.get('address')
            postal = biz_form.cleaned_data.get('postal')
            state = biz_form.cleaned_data.get('state')
            city = biz_form.cleaned_data.get('city')
            notes = booking_form.cleaned_data.get('notes')

            subdomain = request.POST.get('subdomain', company.slug)
            returning = request.POST.get('returning', False)
            
            status = 'published'
            company.description = description
            company.address = address
            company.postal = postal
            company.state = state
            company.city = city
            company.status = status
            if returning:
                company.returning = True
            company.notes = notes
            if subdomain != company.slug:
                if not Company.objects.filter(slug=subdomain).exists():
                    company.slug = slugify(subdomain)
            try:
                company.background = 'carbon'
                company.save()
            except ValueError:
                biz_form.add_error('address','Check your address again. Could not find the location.')
                biz_form.add_error('postal','Check your postal code')
                biz_form.add_error('city','Check the city')
                return render(request, 'productadmin/dashboard/profile/addcompany.html', {'booking_form':booking_form,'biz_form':biz_form, 'addon_form':addon_form, 'product_form':product_form,'company':company,})
            user.on_board = True
            user.save()
            
            bizCreatedEmailSent.delay(user.id)
            return redirect(reverse('home', host='prodadmin'))
        else:
            print(booking_form.errors)
    company = Company.objects.get(user=user)

    return render(request, 'productadmin/dashboard/profile/addcompany.html', {'booking_form':booking_form,'biz_form':biz_form, 'addon_form':addon_form, 'product_form':product_form,'company':company,})

def load_subcat(request):
    cat_id = request.GET.get('category')
    if cat_id:
        subcategories = SubCategory.objects.filter(category_id=cat_id).order_by('name')
    else:
        subcategories = None
    return render(request, 'bizadmin/dashboard/profile/addcompanyhelper/subcat_dropdown_list_options.html', {'subcategories': subcategories})

def load_services(request):
    company = Company.objects.get(user=request.user)
    services = company.services_offered.all()
    return render(request, 'bizadmin/dashboard/profile/addcompanyhelper/subcat_dropdown_list_options.html', {'subcategories': services})

def signupViews(request):
    context = {}
    if request.method == 'POST':
        user_form = BusinessRegistrationForm(request.POST)
        biz_name = BusinessName(request.POST)
        if user_form.is_valid() and biz_name.is_valid():
            user_form.save()
            email = user_form.cleaned_data.get('email')
            raw_pass = user_form.cleaned_data.get('password1')
            phone = user_form.cleaned_data.get('phone')
            bname = biz_name.cleaned_data.get('business_name')
            account = authenticate(email=email, password=raw_pass)
            login(request, account)
            company = Company.objects.create(user=account,business_name=bname,email=email,phone=phone,
                                                description='',address='',postal='',
                                                state='',city='',status='draft')
            company.save()
            first = user_form.cleaned_data.get('first_name')
            last = user_form.cleaned_data.get('last_name')

            staff = StaffMember.objects.create(company=company, user=account, first_name=first, last_name=last, phone=phone, email=email,slug=first,login=True,access=2)
            staff.save()
            biz_hours = OpeningHours.objects.bulk_create([
                OpeningHours(company=company, weekday=0,is_closed=True),
                OpeningHours(company=company, weekday=1,is_closed=False),
                OpeningHours(company=company, weekday=2,is_closed=False),
                OpeningHours(company=company, weekday=3,is_closed=False),
                OpeningHours(company=company, weekday=4,is_closed=False),
                OpeningHours(company=company, weekday=5,is_closed=False),
                OpeningHours(company=company, weekday=6,is_closed=True),
            ])

            staff_hours = StaffWorkingHours.objects.bulk_create([
                StaffWorkingHours(staff=staff, weekday=0,is_off=True),
                StaffWorkingHours(staff=staff, weekday=1,is_off=False),
                StaffWorkingHours(staff=staff, weekday=2,is_off=False),
                StaffWorkingHours(staff=staff, weekday=3,is_off=False),
                StaffWorkingHours(staff=staff, weekday=4,is_off=False),
                StaffWorkingHours(staff=staff, weekday=5,is_off=False),
                StaffWorkingHours(staff=staff, weekday=6,is_off=True),
            ])
            return redirect(reverse('completeprofile', host='prodadmin'))
        else:
            context['business_registration_form'] = user_form
            context['business'] = biz_name
    else:
        user_form = BusinessRegistrationForm()
        biz_name = BusinessName()
        context['business_registration_form'] = user_form
    return render(request, 'accountprod/bussignup.html', {'user_form':user_form, 'biz_name':biz_name,'none':'d-none'})

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
                        return redirect(reverse('home', host='prodadmin'))
                    else:
                        return redirect(reverse('completeprofile', host='prodadmin'))
                        
                else:
                    return redirect(reverse('newbizcreate', host='prodadmin'))
        else:
            context['business_registration_form'] = user_form
            
    else:
        user_form = AccountAuthenticationForm()
        context['business_registration_form'] = user_form
    return render(request, 'accountprod/buslogin.html', {'user_form':user_form, 'none':'d-none'})

def profileViews(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            image_form = MainPhoto()
            personal_data = {'first_name': user.first_name, 
                    'last_name': user.last_name, 
                    'email':user.email, 
                    'phone':user.phone}
            personal_form = UpdatePersonalForm(initial=personal_data)
            return render(request, 'productadmin/dashboard/account/profile.html',{'company':company, 'image_form':image_form, 'personal_form':personal_form})
        else:
            return redirect(reverse('completeprofile', host='prodadmin'))
    else:
        loginViews(request)
    
class personDetailSave(View):
    def post(self, request):
        personal_form = UpdatePersonalForm(request.POST, instance=request.user)
        acct = get_object_or_404(Account, email=request.user)
        staff = get_object_or_404(StaffMember, user=acct)
        if personal_form.is_valid():
            acct.first_name = personal_form.cleaned_data.get('first_name')
            acct.last_name = personal_form.cleaned_data.get('last_name')
            acct.email = personal_form.cleaned_data.get('email')
            acct.phone = personal_form.cleaned_data.get('phone')
            acct.save()
            staff.first_name = personal_form.cleaned_data.get('first_name')
            staff.last_name = personal_form.cleaned_data.get('last_name')
            staff.email = personal_form.cleaned_data.get('email')
            staff.phone = personal_form.cleaned_data.get('phone')
            staff.save()

            return JsonResponse({'good':"The data was good"})

        else:
            return JsonResponse({'errors':'There were errors'})

@login_required()
def profileSecurityViews(request):
    company = get_object_or_404(Company, user=request.user)
    user=request.user
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    elif not user.is_business:
        loginViews(request)
    return render(request,'productadmin/dashboard/account/security.html', {'company':company})

import weasyprint
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    company = order.company
    if request.user != 'sdonald@gibele.com':
        return redirect(reverse('home', host='prodadmin'))
    html = render_to_string('productemail/invoice.html',{'order':order, 'company':company})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response


@login_required()
def notifViews(request):
    company = get_object_or_404(Company, user=request.user)
    user=request.user
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    elif not user.is_business:
        loginViews(request)
    notesForm = AddNotesForm(initial={'notes':company.notes})
    return render(request,'productadmin/dashboard/account/notification.html', {'company':company, 'notesForm':notesForm})

class updateEmailSetting(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['emailReminder']
        company = get_object_or_404(Company, user=request.user)
        if email == True:
            company.emailReminders = True
        else:
            company.emailReminders = False
        company.save()

        return JsonResponse({'good':'girl'})

class notesUpdate(View):
    def post(self, request):
        data = json.loads(request.body)
        notesShow = data['isnotes']
        company  = get_object_or_404(Company, user=request.user)
        notes = data['notes']
        company.notes = notes
        # print(notes)
        if notesShow:
            company.shownotes = True
        else:
            company.shownotes = False
        company.save()

        return JsonResponse({'good':'success'})

from products.tasks import *
class modalGetOrderType(View):
    def get(self, request):
        user = request.user
        company = Company.objects.get(user=user)
        order_id = request.GET.get('order')
        type_of_req = request.GET.get('type')
        order = Order.objects.get(pk=str(order_id))
        html = ''
        title = ''
        if company != order.company:
            return JsonResponse({'html_form':html, 'title':title})
        if type_of_req == 'detail':
            for items in order.items.all():
                name = items.product.name
            title = 'Order: ' + name
            html = render_to_string('productadmin/dashboard/orders/partials/view_details.html', {'order':order, 'company':company}, request=request)
        return JsonResponse({'html_form':html, 'title':title})

    def post(self, request):
        user = request.user
        company = Company.objects.get(user=user)
        order_id = request.POST.get('order')
        type_of_req = request.POST.get('type')
        order = Order.objects.get(pk=str(order_id))
        html = ''
        title = ''
        txt = ''
        if company != order.company:
            return JsonResponse({'type':'error', 'txt':'There was an error'})

        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
        payment_intent_id = order.paymentintent

        if payment_intent_id is None:
            return JsonResponse({'type':'error', 'txt':'There was an error, payment does not exist.'})
        
        if type_of_req == 'accept':
            try:
                stripe.PaymentIntent.capture(
                    payment_intent_id,
                    stripe_account=company.stripe_user_id_prod
                )
                payintent = stripe.PaymentIntent.retrieve(
                    payment_intent_id,
                    stripe_account=company.stripe_user_id_prod
                )

            except Exception as e:
                print(e)
                return JsonResponse({'type':'error', 'txt':'There was an error, unable to collect the payment.'})
            if payintent.status == 'succeeded':
                order.active = True
                order.paid = True
                order.pendingapproval = False
                order.save()
                title = 'The order has been accepted and payment was collected'
                order_request_accepted.delay(order.id)
            else:
                return JsonResponse({'type':'error', 'txt':'There was an error, unable to collect the payment.'})
        #Decline the order request
        elif type_of_req == 'decline':
            if order.paid == True:
                order.pendingapproval = False
                order.save()
                return JsonResponse({'type':'error', 'txt':'There was an error, the payment was already collected.'})
            try:
                payintent = stripe.PaymentIntent.cancel(
                    payment_intent_id,
                    stripe_account=company.stripe_user_id_prod
                )
            except Exception as e:
                print(e)
                return JsonResponse({'type':'error', 'txt':'There was an error, please contact shopme support.'})
            title = 'The order has been declined and payment was cancelled.'
            txt = 'This action can not be undone.'
            order.active = False
            order.paid = False
            order.pendingapproval = False
            order.cancelled = True
            order.save()
            order_request_cancelled.delay(order.id)
        elif type_of_req == 'cancel':
            try:
                payintent = stripe.Refund.create(
                    refund_application_fee=True,
                    payment_intent=payment_intent_id,
                    stripe_account=company.stripe_user_id_prod
                )
            except Exception as e:
                print(e)
                return JsonResponse({'type':'error', 'txt':'There was an error, please contact shopme support.'})
            order.paid = False
            order.pendingapproval = False
            order.cancelled = True
            order.active = False
            title = 'The order has been cancelled and payment was refunded.'
            txt = 'This action can not be undone.'
            order.save()
            order_payment_cancelled.delay(order.id)
        elif type_of_req == 'fulfill':
            order.paid = True
            order.pendingapproval = False
            order.active = False
            order.completed = True
            order_total_completed.delay(order.id)
            title = 'The order has been marked as completed!'
        order.save()
        return JsonResponse({'title':title, 'type':'success', 'txt':txt})


@login_required
def orderView(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            day = datetime.today().weekday() + 1
            if day >= 7:
                day = 0
            openhour = OpeningHours.objects.get(company=company, weekday=day).from_hour
            search = request.GET.get('search')
            pending = False
            completed = False
            upcoming = False
            cancelled = False
            active = False
            delivered=False
            types = ''
            if search == 'pending':
                orders = Order.objects.filter(company=company, orderplaced=True,pendingapproval=True, completed=False, cancelled=False).order_by('-created')
                pending = True
                types = 'pending'
            elif search == 'completed':
                orders = Order.objects.filter(company=company, paid=True, orderplaced=True,pendingapproval=False, completed=True, cancelled=False).order_by('-created')
                completed = True
                types = 'completed'
            elif search == 'cancelled':
                orders = Order.objects.filter(company=company, orderplaced=True, cancelled=True).order_by('-created')
                cancelled = True
            elif search == 'active':
                orders = Order.objects.filter(company=company, orderplaced=True, active=True, pendingapproval=False).order_by('-created')
                active = True
                types = 'active'
            elif search == 'delivered':
                orders = Order.objects.filter(company=company, orderplaced=True, delivered=True).order_by('-created')
                delivered = True
                types = 'delivered'
            else:
                orders = Order.objects.filter(company=company, orderplaced=True).order_by('-created')
                upcoming = True
                types = 'all'

            paginator = Paginator(orders, 5)
            page = request.GET.get('page')
            try:
                orders = paginator.page(page)
            except PageNotAnInteger:
                orders = paginator.page(1)
            except EmptyPage:
                orders = paginator.page(paginator.num_pages)
            return render(request, 'productadmin/dashboard/orders/orders_upcoming.html', {
                                                                                            'types':types,
                                                                                            'page':page,
                                                                                            'company':company, 
                                                                                            'orders':orders, 
                                                                                            'pending':pending, 
                                                                                            'completed':completed, 
                                                                                            'upcoming':upcoming, 
                                                                                            'cancelled':cancelled,
                                                                                            'active':active,
                                                                                            'delivered':delivered
                                                                                        })
        else:
            return redirect(reverse('completeprofile', host='prodadmin'))
    else:
        loginViews(request)

from .forms import ShippingZoneForm, PriceBasedShippingRateForm
@login_required
def shippingView(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            return render(request, 'productadmin/dashboard/shipping/shipping.html', {
                                                                                        'company':company
                                                                                    })
        else:
            return redirect(reverse('completeprofile', host='prodadmin'))
    else:
        loginViews(request)

from .models import CompanyShippingZone, PriceBasedShippingRate

@login_required
def addshippingView(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            # zone = CompanyShippingZone.objects.create(company=company, name='')
            form = ShippingZoneForm()
            pricebasedform = PriceBasedShippingRateForm()
            return render(request, 'productadmin/dashboard/shipping/shipping_zone/addshippingzone.html', {
                                                                                        'company':company,
                                                                                        'form':form,
                                                                                        'pricebasedform':pricebasedform
                                                                                    })
        else:
            return redirect(reverse('completeprofile', host='prodadmin'))
    else:
        loginViews(request)
from django_countries import countries as countriesfields
class createshippingZoneViewAPI(View):
    def post(self,request):
        company = Company.objects.get(user=request.user)
        form = ShippingZoneForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            countries = request.POST.getlist('countryinput')
            pricebased = request.POST.getlist('pricebasedid')
            allcountry = False
            zone = CompanyShippingZone.objects.create(name=name, company=company)
            for c in countries:
                if c == 'all':
                    allcountry = True
                    break
                else:
                    break
            if allcountry:
                zone.country = list(countriesfields)
            else:
                zone.country = countries
            for c in pricebased:
                zone.pricebased_rate.add(PriceBasedShippingRate.objects.get(pk=c))
            zone.save()
            return redirect(reverse('shipping', host='prodadmin'))
        else:
            return render(request, 'productadmin/dashboard/shipping/shipping_zone/addshippingzone.html', {
                                                                                        'company':company,
                                                                                        'form':form
                                                                                    })

class createPBRShippingViewAPI(View):
    def post(self,request):
        company = Company.objects.get(user=request.user)
        form = PriceBasedShippingRateForm(request.POST)
        error = False
        html_content = ''
        if form.is_valid():
            upper_price = form.cleaned_data.get('upper_price')
            lower_price = form.cleaned_data.get('lower_price')
            name = form.cleaned_data.get('names')
            rate = form.cleaned_data.get('rate')
            ids = None
            if PriceBasedShippingRate.objects.filter(names=name,company=company).exists():
                error = 'This rate name has already been used. Please try a different rate name.'
            elif upper_price is None:
                ids = PriceBasedShippingRate.objects.create(names=name,rate=rate,upper_price=upper_price,lower_price=lower_price,company=company)
                ids = ids.id
            elif upper_price < lower_price:
                error = 'Please make sure the minimum order price is less than the maximum order price.'
            else:
                ids = PriceBasedShippingRate.objects.create(names=name,rate=rate,upper_price=upper_price,lower_price=lower_price,company=company)
                ids = ids.id
            html_content = render_to_string('productadmin/dashboard/shipping/partial/pricebased_rate.html', {'my_id':ids, 'company':company})
        else:
            error = 'There was an error, please double check the values'
            for err in form.errors:
                if err == 'lower_price':
                    error = 'Please ensure the minimum order price is greater or equal than $0.00'
                elif err == 'upper_price':
                    error = 'Please ensure the maximum order price is greater or equal than $0.01'
                else:
                    error = 'Please ensure the rate amount is greater or equal to $0.00'
        return JsonResponse({'error':error, 'html_content':html_content})

from django_countries import countries
class getCountriesListAPI(View):
    def get(self,request):
        company = Company.objects.get(user=request.user)
        countries = request.GET.getlist('data[]')
        allcountry = False
        for c in countries:
            if c == 'all':
                countries = ['all']
                break
            else:
                break
        html_response = render_to_string('productadmin/dashboard/shipping/partial/countries.html', {'countriess':countries, 'company':company})
        return JsonResponse({'html_content':html_response})

def fileUploadView(request):
    if request.POST:
        return JsonResponse({'works':'works'})

def LogoutView(request):
    logout(request)
    return redirect(reverse('bizadminmain', host='prodadmin'))


from django.template.loader import render_to_string
def save_service_form(request, form, template_name):
    data=dict()
    company = Company.objects.get(user=request.user)
    if request.method=='POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            price = form.cleaned_data.get('price')
            mainimage = form.cleaned_data.get('mainimage')
            dispatch = form.cleaned_data.get('dispatch')
            is_requested = request.POST.get('requestedinput')
            if is_requested is not None:
                is_requested = True
            else:
                is_requested = False
            avail = True
            company = Company.objects.get(user=request.user)
            product = ProductModel.objects.create(business=company,name=name,description=description, price=price, mainimage=mainimage, stock=1, dispatch=dispatch, request=is_requested)
            product.save()
            user = request.user
            data['form_is_valid'] = True
            product = ProductModel.objects.filter(business=company)
            #Temp Solution
            request.session['formsuccess'] = 'Your product has been created!'
            return redirect(reverse('service_detail', host='prodadmin'))
        else:
            print(form.errors)
            request.session['formerror'] = 'There was an error creating your product. Please ensure all values are entered correctly.'
            data['form_is_valid'] = False
    return redirect(reverse('service_detail', host='prodadmin'))

#used in the onboarding page
def createproductViews(request):
    if request.method=='POST':
        service_form = AddProductForm(request.POST, request.FILES)
    else:
        service_form = AddProductForm()
    return save_service_form(request, service_form, 'productadmin/dashboard/profile/services/partial_service_create.html')

#used in the bizadmin page
class createserviceAPI(View):
    def post(self,request):
        company = Company.objects.get(user=request.user)
        form = AddServiceForm(request.POST)
        form2 = AddServiceToCategory(request.POST, initial={'company':company})
        data = dict()
        if form.is_valid() and form2.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_type = form.cleaned_data.get('price_type')
            is_requested = form.cleaned_data.get('is_request')
            price = form.cleaned_data.get('price')
            duration_hour = form.cleaned_data.get('duration_hour')
            duration_minute = form.cleaned_data.get('duration_minute')
            checkintime=form.cleaned_data.get('checkintime')
            padding=form.cleaned_data.get('padding')
            paddingtime_hour=form.cleaned_data.get('paddingtime_hour')
            paddingtime_minute=form.cleaned_data.get('paddingtime_minute')
            avail = True
            if is_requested == 'n':
                requ = False
            else:
                requ = True
            service = Services.objects.create(business=company,name=name,description=description,price=price, available=avail, 
                                                price_type=price_type,duration_hour=duration_hour,duration_minute=duration_minute,checkintime=checkintime,
                                                padding=padding,paddingtime_hour=paddingtime_hour,paddingtime_minute=paddingtime_minute, request=requ)
            service.save()

            catename = form2.cleaned_data.get('category')
            for cate in catename:
                sc = ServiceCategories.objects.get(name=cate.name, company=company)
                sc.services.add(service)
            staffname = form2.cleaned_data.get('staff')
            for staff in staffname:
                staffmem = StaffMember.objects.get(id=staff.id)
                staffmem.services.add(service)

            formfieldname = form2.cleaned_data.get('formfield')
            for ff in formfieldname:
                formfields = formBuilder.objects.get(id=ff.id)
                formfields.services.add(service)

            data['form_is_valid'] = True
            data['view'] = 'Your service has been created!'
            data['icon'] = 'success'
        else:
            data['form_is_valid'] = False
            data['view'] = 'Your service was not created. There was an error.'
            data['icon'] = 'error'
        company = Company.objects.get(user=request.user)
        services = Services.objects.filter(business=company)
        paginator = Paginator(services, 5)
        page = request.GET.get('page')
        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)
        data['html_service_list'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_list.html', {'page':page,'services':services, 'company':company})
        data['html_category_list'] = render_to_string('bizadmin/companydetail/services/partial_category/category_list.html',{'company':company})
        return JsonResponse(data)

class deleteCategoryAPI(View):
    def post(self, request, pk):
        ServiceCategories.objects.get(pk=pk).delete()
        company = Company.objects.get(user=request.user)
        services = Services.objects.filter(business=company)
        paginator = Paginator(services, 5)
        page = request.GET.get('page')
        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)
        data=dict()
        data['html_service_list'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_list.html', {'page':page,'services':services, 'company':company})
        data['html_category_list'] = render_to_string('bizadmin/companydetail/services/partial_category/category_list.html',{'company':company})
        return JsonResponse(data)

class createserviceAPII(View):
    def get(self, request, pk):
        company = Company.objects.get(user=request.user)
        if int(pk)==0:
            sc = company.product_category.none()
            allstaff = company.staffmembers.none()
            allformfields = company.company_forms.none()
        else:
            sc = company.product_category.filter(id=pk)
        form = AddProductForm()
        form2 = AddServiceToCategory(initial={'company':company, 'category':sc, 'staff':allstaff, 'formfield':allformfields})
        context = {'company':company}
        html2 = render_to_string('bizadmin/companydetail/services/partial_category/category_list.html', context, request=request)
        context = {'service_form':form, 'category_form':form2,'company':company}
        html = render_to_string('bizadmin/companydetail/services/partial/partial_service_create.html', context, request=request)
        return JsonResponse({'html_form':html, 'html_category':html2})


class createcategoryAPI(View):
    def post(self, request):
        company = Company.objects.get(user=request.user)
        form = AddServiceCategoryForm(request.POST, initial={'company':company})
        data = dict()
        if form.is_valid():
            name = form.cleaned_data['name']
            services = form.cleaned_data.get('services')
            if not ServiceCategories.objects.filter(name=name, company=company).exists():
                sc = ServiceCategories.objects.create(name=name, company=company)
            else:
                sc = ServiceCategories.objects.get(name=name, company=company)
            for s in services:
                sc.services.add(s)
            sc.save()

        services = Services.objects.filter(business=company)
        paginator = Paginator(services, 5)
        page = request.GET.get('page')
        try:
            services = paginator.page(page)
        except PageNotAnInteger:
            services = paginator.page(1)
        except EmptyPage:
            services = paginator.page(paginator.num_pages)

        data=dict()
        data['html_service_list'] = render_to_string('bizadmin/companydetail/services/partial/partial_service_list.html', {'page':page,'services':services, 'company':company})
        data['html_category_list'] = render_to_string('bizadmin/companydetail/services/partial_category/category_list.html',{'company':company})
        data['view'] = 'Service Category has been created'
        data['icon'] ='success'

        return JsonResponse(data)

class createclientAPI(View):
    def post(self,request):
        form = AddClientForm(request.POST)
        data = dict()
        if form.is_valid():
            company = Company.objects.get(user=request.user)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone = form.cleaned_data.get('phone')
            email = form.cleaned_data.get('email')
            address = form.cleaned_data.get('address')
            postal = form.cleaned_data.get('postal')
            city = form.cleaned_data.get('city')
            province = form.cleaned_data.get('province')
            user = None
            if email:
                if Account.objects.filter(email = email).exists():
                    user = Account.objects.get(email=email)
            elif phone:
                if Account.objects.filter(phone=phone).exists():
                    user = Account.objects.filter(phone=phone).first()
            
            Clients.objects.create(user=user, company=company, first_name=first_name, last_name=last_name, email=email,phone=phone,
                                city=city,postal=postal,province=province,address=address)
            clients = company.clients.all()
            data['form_is_valid'] = True
            data['view'] = 'Your client has been added!'
            data['icon'] = 'success'
        else:
            data['form_is_valid'] = False
            data['view'] = 'Your client was not added. There was an error.'
            data['icon'] = 'error'
        data['html_service_list'] = render_to_string('bizadmin/companydetail/client/partial/partial_client_list.html', {'clients':clients, 'company':company})
        return JsonResponse(data)

class deleteclientAPI(View):
    def get(self, request, pk):
        data = dict()
        company = Company.objects.get(user=request.user)
        client = get_object_or_404(Clients, pk=pk, company=company)
        client.delete()
        clients = company.clients.all()
        data['html_service_list'] = render_to_string('bizadmin/companydetail/client/partial/partial_client_list.html', {'clients':clients})
        return JsonResponse(data)


#used in the bizadmin page
class deleteserviceAPI(View):
    def post(self, request, pk):
        data = dict()
        company = Company.objects.get(user=request.user)
        product = get_object_or_404(ProductModel, pk=pk, business=company)
        product.delete()
        services = ProductModel.objects.filter(business=company)
        data['html_product_list'] = render_to_string('productadmin/companydetail/services/partial/partial_service_list.html', {'services':services, 'company':company})
        # data['html_category_list'] = render_to_string('bizadmin/companydetail/services/partial_category/category_list.html',{'company':company})
        return JsonResponse(data)

#Used in the bizadmin page
class updateserviceAPI(View):
    def get(self, request, pk):
        product = get_object_or_404(ProductModel, pk=pk)
        company = Company.objects.get(user=request.user)
        dat = {
                'name': product.name, 
                'description': product.description,
                'price':product.price, 
                'mainimage':product.mainimage,
                'dispatch':product.dispatch,
                'request':product.request,
            }
        data=dict()
        form = AddProductForm(initial=dat)
        
        context = {'product_form':form, 'product':product,'company':company}
        data['html_form'] = render_to_string('productadmin/companydetail/services/partial/partial_service_update.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, pk):
        product = get_object_or_404(ProductModel, pk=pk)
        company = Company.objects.get(user=request.user)
        form = AddProductForm(request.POST, request.FILES)
        data=dict()
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            price = form.cleaned_data.get('price')
            mainimage = form.cleaned_data.get('mainimage')
            dispatch = form.cleaned_data.get('dispatch')
            is_requested = request.POST.get('requestedinput')
            is_clear = request.POST.get('mainimage-clear')
            if is_requested is not None:
                is_requested = True
            else:
                is_requested = False
            if is_clear is not None:
                is_clear = True
            else:
                is_clear = False
            avail = True
            product.name = name
            product.request = is_requested
            product.description = description
            product.price = price
            product.dispatch = dispatch
            if mainimage:
                product.mainimage = mainimage
            if is_clear:
                product.mainimage = ''
            product.save()
            user = request.user
            data['form_is_valid'] = True
            request.session['formsuccess'] = product.name + ' product has been updated.'
            #Temp Solution
            return redirect(reverse('service_detail', host='prodadmin'))
            
        else:
            request.session['formerror'] = 'There was an error updating your product. Please ensure all values are entered correctly.'
            data['form_is_valid'] = False
            return redirect(reverse('service_detail', host='prodadmin'))

from django.forms import formset_factory
class addQuestionOption(View):
    def get(self, request, pk):
        product = get_object_or_404(ProductModel, pk=pk)
        company = Company.objects.get(user=request.user)
        form = questionProductForm()
        data=dict()
        context = {'question_form':form,'product':product,'company':company}
        data['html_form'] = render_to_string('productadmin/companydetail/services/partial/partial_question_form.html', context, request=request)
        return JsonResponse(data)
    def post(self, request, pk):
        product = get_object_or_404(ProductModel, pk=pk)
        company = Company.objects.get(user=request.user)
        if product.business != company:
            return redirect(reverse('service_detail', host='prodadmin'))
        form = questionProductForm(request.POST)
        is_required = request.POST.get('requiredinput')
        if is_required is not None:
            is_required = True
        else:
            is_required = False
        
        if form.is_valid():
            question = form.cleaned_data.get('question')
            placeholder = form.cleaned_data.get('placeholder')
            retrievetype = form.cleaned_data.get('retrievetype')
            QuestionModels.objects.create(question=question, is_required=is_required, product=product, placeholder=placeholder,retrievetype=retrievetype)
            request.session['formsuccess'] = 'Your question has been attached to ' + product.name + '.'
        else:
            request.session['formerror'] = 'There was an error attaching the question to your product. The question can be a maximum 400 characters.'
            return redirect(reverse('service_detail', host='prodadmin'))
        return redirect(reverse('service_detail', host='prodadmin'))

class addProductGallaryPic(View):
    def get(self, request, pk):
        product = get_object_or_404(ProductModel, pk=pk)
        company = Company.objects.get(user=request.user)
        form = dropDownForm()
        form2 = formset_factory(dropDownOptionsForm, extra=2)
        data=dict()
        context = {'placeholder_form':form, 'option_form':form2,'product':product,'company':company}
        data['html_form'] = render_to_string('productadmin/companydetail/services/partial/partial_dropdown_form.html', context, request=request)
        return JsonResponse(data)

class addDropdownOption(View):
    def get(self, request, pk):
        product = get_object_or_404(ProductModel, pk=pk)
        company = Company.objects.get(user=request.user)
        form = dropDownForm()
        form2 = formset_factory(dropDownOptionsForm, extra=2)
        data=dict()
        context = {'placeholder_form':form, 'option_form':form2,'product':product,'company':company}
        data['html_form'] = render_to_string('productadmin/companydetail/services/partial/partial_dropdown_form.html', context, request=request)
        return JsonResponse(data)
    def post(self, request, pk):
        product = get_object_or_404(ProductModel, pk=pk)
        company = Company.objects.get(user=request.user)
        if product.business != company:
            return redirect(reverse('service_detail', host='prodadmin'))
        form = dropDownForm(request.POST)
        DropDownOptionFormSet = formset_factory(dropDownOptionsForm, extra=2)
        formset = DropDownOptionFormSet(request.POST)
        is_required = request.POST.get('requiredinput')
        is_multiple = request.POST.get('multiplechoices')
        if is_required is not None:
            is_required = True
        else:
            is_required = False

        if is_multiple is not None:
            is_multiple = True
        else:
            is_multiple = False
        
        if formset.is_valid() and form.is_valid():
            dropdownname = form.cleaned_data.get('placeholder')
            mpdd = MainProductDropDown.objects.create(placeholder=dropdownname, is_required=is_required,is_multiple=is_multiple, product=product)
            for forms in formset:
                option = forms.cleaned_data.get('option')
                price = forms.cleaned_data.get('price')
                if price is None:
                    price = 0.00
                if option is not None:
                    ProductDropDown.objects.create(option=option, price=price, dropdown=mpdd)
            request.session['formsuccess'] = ' A dropdown option has been added to ' + product.name + '.'
        else:
            request.session['formerror'] = 'There was an error adding the dropdown option to your product. Please ensure all values are entered correctly.'
            return redirect(reverse('service_detail', host='prodadmin'))
        return redirect(reverse('service_detail', host='prodadmin'))

class updateDropDownOption(View):
    def get(self, request, pk):
        product = get_object_or_404(ProductModel, pk=pk)
        company = Company.objects.get(user=request.user)
        form = dropDownForm()
        form2 = formset_factory(dropDownOptionsForm, extra=2)
        data=dict()
        context = {'placeholder_form':form, 'option_form':form2,'product':product,'company':company}
        data['html_form'] = render_to_string('productadmin/companydetail/services/partial/partial_dropdown_form.html', context, request=request)
        return JsonResponse(data)

class removeDropDownOption(View):
    def post(self, request, pk):
        mpdd = MainProductDropDown.objects.get(pk=pk)
        company = Company.objects.get(user=request.user)
        if mpdd.product.business == company:
            mpdd.delete()
        services = ProductModel.objects.filter(business=company)
        data = dict()
        data['html_product_list'] = render_to_string('productadmin/companydetail/services/partial/partial_service_list.html', {'services':services, 'company':company})
        return JsonResponse(data)

class removeQuestionOption(View):
    def post(self, request, pk):
        mpdd = QuestionModels.objects.get(pk=pk)
        company = Company.objects.get(user=request.user)
        if mpdd.product.business == company:
            mpdd.delete()
        services = ProductModel.objects.filter(business=company)
        data = dict()
        data['html_product_list'] = render_to_string('productadmin/companydetail/services/partial/partial_service_list.html', {'services':services, 'company':company})
        return JsonResponse(data)




## Adding the homepage views and all stuff required for the homepage
from django.utils import timezone
import pytz
from datetime import timedelta, datetime
from django.db.models import Sum
from decimal import Decimal
from taggit.models import Tag
@login_required
def homepageViews(request):
    user = request.user
    if user.is_authenticated and user.is_business:
        if user.on_board:
            company = Company.objects.get(user=user)
            #Percentage for business page photos
            bpp = 0
            #Client added to the database percentage
            cdb = 0
            #Products added to the database percentage
            sdb = 0
            #Tags add to the database
            tpp = 0
            #Link the stripe payment processing to company
            spp =0

            #Total Basic Account Setup
            if company.tags.all(): 
                tpp = 100

            if company.stripe_access_token_prod:
                spp = 100
            
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
            
            products = ProductModel.objects.filter(business=company)

            for product in products:
                sdb = sdb + 25
                if sdb >= 100:
                    sdb = 100
                    break
            
            ttpp = int((bpp/4)+ (sdb/4) + (tpp/4) + (spp/4)) 
            week = timezone.localtime(timezone.now() - timedelta(days=7))
            twoweek = week - timedelta(days=7)
            threeweek = twoweek - timedelta(days=7)
            fourweek = threeweek - timedelta(days=7)
            week1 = Order.objects.filter(company=company, created__gte=week, created__lte=timezone.now(),paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not week1:
                week1 = 0
            start1 = (week - timedelta(days=week.weekday())).strftime("%b-%d-%Y")
            
            week2 = Order.objects.filter(company=company, created__gte=twoweek, created__lte=week,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not week2:
                week2 = 0
            start2 = (twoweek - timedelta(days=twoweek.weekday())).strftime("%b-%d-%Y")

            week3 = Order.objects.filter(company=company, created__gte=threeweek, created__lte=twoweek,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not week3:
                week3 = 0
            start3 = (threeweek - timedelta(days=threeweek.weekday())).strftime("%b-%d-%Y")

            week4 = Order.objects.filter(company=company, created__gte=fourweek, created__lte=threeweek,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not week4:
                week4 = 0
            start4 = (fourweek - timedelta(days=fourweek.weekday())).strftime("%b-%d-%Y")
            week = [int(week4), int(week3), int(week2), int(week1)]
            weeklabel = [start4, start3, start2, start1]

            month = timezone.localtime(timezone.now() - timedelta(days=30))
            month1 = Order.objects.filter(company=company, created__gte=month, created__lte=timezone.now(),paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month1:
                month1 = 0
            labelM0 = timezone.now().strftime("%b-%Y")
            labelM1 = month.strftime("%b-%Y")

            twomonth = month - timedelta(days=30)
            month2 = Order.objects.filter(company=company, created__gte=twomonth, created__lte=month,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month2:
                month2 = 0
            labelM2 = twomonth.strftime("%b-%Y")

            threemonth = twomonth - timedelta(days=30)
            month3 = Order.objects.filter(company=company, created__gte=threemonth, created__lte=twomonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month3:
                month3 = 0
            labelM3 = threemonth.strftime("%b-%Y")

            fourmonth = threemonth - timedelta(days=30)
            month4 = Order.objects.filter(company=company, created__gte=fourmonth, created__lte=threemonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month4:
                month4 = 0
            labelM4 = fourmonth.strftime("%b-%Y")

            fivemonth = fourmonth - timedelta(days=30)
            month5 = Order.objects.filter(company=company, created__gte=fivemonth, created__lte=fourmonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month5:
                month5 = 0
            labelM5 = fivemonth.strftime("%b-%Y")

            sixmonth = fivemonth - timedelta(days=30)
            month6 = Order.objects.filter(company=company, created__gte=sixmonth, created__lte=fivemonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month6:
                month6 = 0
            labelM6 = sixmonth.strftime("%b-%Y")

            sevenmonth = sixmonth - timedelta(days=30)
            month7 = Order.objects.filter(company=company, created__gte=sevenmonth, created__lte=sixmonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month7:
                month7 = 0
            labelM7 = sevenmonth.strftime("%b-%Y")

            eightmonth = sevenmonth - timedelta(days=30)
            month8 = Order.objects.filter(company=company, created__gte=eightmonth, created__lte=sevenmonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month8:
                month8 = 0
            labelM8 = eightmonth.strftime("%b-%Y")

            ninemonth = eightmonth - timedelta(days=30)
            month9 = Order.objects.filter(company=company, created__gte=ninemonth, created__lte=eightmonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month9:
                month9 = 0
            labelM9 = ninemonth.strftime("%b-%Y")

            tenmonth = ninemonth - timedelta(days=30)
            month10 = Order.objects.filter(company=company, created__gte=tenmonth, created__lte=ninemonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month10:
                month10 = 0
            labelM10 = tenmonth.strftime("%b-%Y")

            elevenmonth = tenmonth - timedelta(days=30)
            month11 = Order.objects.filter(company=company, created__gte=elevenmonth, created__lte=tenmonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month11:
                month11 = 0
            labelM11 = elevenmonth.strftime("%b-%Y")

            twelvemonth = elevenmonth - timedelta(days=30)
            month12 = Order.objects.filter(company=company, created__gte=twelvemonth, created__lte=elevenmonth,paid=True).aggregate(Sum('items__price')).get('items__price__sum',0)
            if not month12:
                month12 = 0
            labelM12 = twelvemonth.strftime("%b-%Y")

            month = [int(month12),int(month11),int(month10),int(month9),int(month8),int(month7),int(month6),int(month5),int(month4),int(month3),int(month2),int(month1),]
            monthlabel = [labelM12,labelM11,labelM10,labelM9,labelM8,labelM7,labelM6,labelM5,labelM4,labelM3,labelM2,labelM1]
            return render(request,'productadmin/home/home.html', {'ttpp':ttpp,'tpp':tpp,'sdb':sdb,'cdb':cdb,'company':company, 'week':week, 'weeklabel':weeklabel, 'month':month, 'monthlabel':monthlabel, 'bpp':bpp})
        else:
            return redirect(reverse('completeprofile', host='prodadmin'))
    else:
        loginViews(request)

from PIL import Image
from django.core.files import File
from io import BytesIO
from django.core.files.base import ContentFile


@login_required
def profileImageUpload(request):
    if request.POST:
        user = Account.objects.get(email=request.user)
        img = request.FILES.get('imageFile')

        valid_extensions = ['jpg', 'png', 'jpeg']
        extension = img.name.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            return JsonResponse({'success':'success'})
        if img:
            image = Image.open(img)
            image.filename = img.name
            minimumsize = min(image.size)
            width, height = image.size
            box = ((width - minimumsize) // 2, (height - minimumsize) // 2, (width + minimumsize) // 2, (height + minimumsize) // 2)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((2048,2048),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image.format)
            user.avatar.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            user.save()
            staffmember = StaffMember.objects.get(user=user)
            staffmember.image.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            staffmember.save()

    
    return JsonResponse({'error':'success', 'append':True})



#For the gallery and photos main photo
@login_required
def headerImageUploads(request):
    if request.POST:
        company = Company.objects.get(user=request.user)
        img = request.FILES.get('imageFile')
        valid_extensions = ['jpg', 'png', 'jpeg']
        extension = img.name.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            return JsonResponse({'success':'success'})
        if img:
            image = Image.open(img)
            image.filename = img.name
            minimumsize = min(image.size)
            width, height = image.size
            box = ((width - minimumsize) // 2, (height - minimumsize) // 2, (width + minimumsize) // 2, (height + minimumsize) // 2)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((2048,2048),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, image.format)
            company.image.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            company.save()
    
    return JsonResponse({'error':'success', 'append':True})
        
def galImageUpload(request):
    if request.POST:
        company = Company.objects.get(user=request.user)
        img = request.FILES.get('kartik-input-700[]')
        # x = Decimal(request.POST.get('xs'))
        # y = Decimal(request.POST.get('ys'))
        # w = Decimal(request.POST.get('widths'))
        # h = Decimal(request.POST.get('heights'))
        valid_extensions = ['jpg', 'png', 'jpeg']
        extension = img.name.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            return JsonResponse({'success':'success'})
        if img:
            image = Image.open(img)
            image.filename = img.name
            width, height = image.size
            aspectratio = height / width
            aspect = int(2048*aspectratio) + 1
            box = (0, 0, width, height)
            cropped_image = image.crop(box)
            resized_image = cropped_image.resize((2048,aspect),Image.ANTIALIAS)
            thumb_io = BytesIO()
            resized_image.save(thumb_io, format=image.format)
            gallary = Gallary.objects.create(company=company)
            gallary.photos.save(image.filename, ContentFile(thumb_io.getvalue()), save=False)
            gallary.save()
    
    return JsonResponse({'success':'success'})
    # return redirect(reverse('photos', host='bizadmin'))

from businessadmin.forms import ImagesForm
##Business Page Views
@login_required
def businessPhotoView(request):
    user=request.user
    company = Company.objects.get(user=user)
    
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    elif not user.is_business:
        loginViews(request)
    photos = Gallary.objects.filter(company=company)
    paginator = Paginator(photos, 200)
    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    return render(request,'productadmin/businesspage/photos.html',{'company':company, 'photos':photos})

@login_required
def businessPageCustomization(request):
    user=request.user
    staff = StaffMember.objects.get(user=request.user)
    company = staff.company
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    elif not user.is_business:
        loginViews(request)
    formBuilderForms = formBuilderForm(initial={'company':company})
    return render(request,'productadmin/businesspage/customization.html',{'company':company, 'formBuilderForms':formBuilderForms})



@login_required
def businessAmenitiesView(request):
    company = Company.objects.get(user=request.user)
    user=request.user
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    elif not user.is_business:
        loginViews(request)
    amenities = Amenities.objects.filter(company=company)
    return render(request,'productadmin/businesspage/amenities.html',{'company':company, 'amenities':amenities})

@login_required
def businessBreaksView(request):
    company = Company.objects.get(user=request.user)
    user=request.user
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    elif not user.is_business:
        loginViews(request)
    return render(request, 'bizadmin/businesspage/hours/breaks-time.html', {'company':company})

@login_required
def businessTimeOffView(request):
    company = Company.objects.get(user=request.user)
    user=request.user
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    elif not user.is_business:
        loginViews(request)
    return render(request, 'bizadmin/businesspage/hours/timeoff.html', {'company':company})

@login_required
def staffMemberView(request):
    company = Company.objects.get(user=request.user)
    user=request.user
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    elif not user.is_business:
        loginViews(request)
    addstaff = StaffMemberForms(initial={'company':company})
    return render(request, 'bizadmin/companydetail/staff/staffmembers.html', {'company':company, 'addstaff':addstaff})


@login_required
def businessHoursView(request):
    company = Company.objects.get(user=request.user)
    sunday = OpeningHours.objects.get(company=company, weekday=0)
    monday = OpeningHours.objects.get(company=company, weekday=1)
    tuesday = OpeningHours.objects.get(company=company, weekday=2)
    wednesday = OpeningHours.objects.get(company=company, weekday=3)
    thursday = OpeningHours.objects.get(company=company, weekday=4)
    friday = OpeningHours.objects.get(company=company, weekday=5)
    saturday = OpeningHours.objects.get(company=company, weekday=6)
    user=request.user
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    elif not user.is_business:
        loginViews(request)
    return render(request, 'bizadmin/businesspage/hours.html', {'company':company,'sunday':sunday, 'monday':monday, 'tuesday':tuesday,'wednesday':wednesday, 'thursday':thursday, 'friday':friday, 'saturday':saturday})


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
from django.contrib.auth import update_session_auth_hash
class updatePassword(View):
    def post(self, request):
        currPass = request.POST.get('currentPassword')
        newPass = request.POST.get('newPassword')
        confirmPass = request.POST.get('confirmPassword')
        user = get_object_or_404(Account, email=request.user)
        if not user.check_password(currPass):
            return JsonResponse({'badresponse':'We could not verify your password. Please try again.'})
        
        if not (newPass==confirmPass):
            return JsonResponse({'badresponse':'Your passwords don\'t match.'})
        password = confirmPass
        length_error = len(password) < 8
        # searching for digits
        digit_error = re.search(r"\d", password) is None
        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None
        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None
        # searching for symbols
        symbol_error = re.search(r"[ !#?<>:$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
        # overall result
        password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )
        if not password_ok:
            return JsonResponse({'badresponse': 'Please enter a stronger password. \nPasswords must be atleast 8 characters long contains atleast 1 digit, a symbol, uppercase and lower case letters.'})
        
        user.set_password(newPass)
        user.save()
        update_session_auth_hash(request, user)
        #Send email to user saying password changed
        return JsonResponse({'good':'We have changed your password successfully!'})

class changePrivateView(View):
    def post(self, request):
        data = json.loads(request.body)
        privacy = data['private']
        company = get_object_or_404(Company, user=request.user)
        if privacy:
            company.status='draft'
        else:
            company.status='published'
        company.save()
        return JsonResponse({'good':'We updated your privacy settings'})

import string
class addAmenityAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['addedAmenity']
        tag = string.capwords(tag)
        company = Company.objects.get(user=request.user)
        company.company_amenity.create(amenity=tag)
        company.save()
        if not tag:
            return JsonResponse({'email_error':'You must choose a subdomain or else a random one will be chosen.','email_valid':True})
        return JsonResponse({'tags':'works'})

class removeAmenityAPI(View):
    def post(self, request):
        data=json.loads(request.body)
        tag = data['removedAmenity']
        company = Company.objects.get(user=request.user)
        amen = company.company_amenity.get(amenity__iexact=tag).delete()

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

@login_required
def compinfoViews(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        biz_name = BusinessName()
        context['business_registration_form'] = user_form
        return render(request, 'accountprod/bussignup.html', {'user_form':user_form,'biz_form':biz_form})
    
    email = request.user.email
    user = get_object_or_404(Account, email=email)

    if not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))

    company = Company.objects.get(user=user)
    subcategory = company.subcategory.filter(category=company.category)
    s = [x.id for x in subcategory]
    initialVal = {'business_name':company.business_name,'slug':company.slug,'email':company.email,'category':company.category, 'description':company.description,
                    'subcategory':s, 'address':company.address, 'postal':company.postal, 'city':company.city, 'state':company.state,
                    'fb_link':company.fb_link,'twitter_link':company.twitter_link,'instagram_link':company.instagram_link,'website_link':company.website_link,'phone':company.phone}
    updateform = UpdateCompanyForm(initial=initialVal)
    return render(request, 'productadmin/companydetail/info/compinfo.html', {'company':company, 'updateform': updateform})

import re
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

class saveCompanyDetail(View):
    def post(self, request):
        company = Company.objects.get(user=request.user)
        post_values = request.POST.copy()
        post_values['category'] = company.category.id
        post_values['subcategory'] = [13]
        form = UpdateCompanyForm(post_values, initial={'category':company.category.id})
        context = {}
        if form.is_valid():
            company.business_name = form.cleaned_data.get('business_name')
            email = form.cleaned_data.get('email')
            subdomain = request.POST.get('subdomain', company.slug)
            if not email==company.email:
                company.email = email
            phone = form.cleaned_data.get('phone')
            if not phone == company.phone:
                company.phone = phone
            if subdomain != company.slug:
                if not Company.objects.filter(slug=subdomain).exists():
                    company.slug = slugify(subdomain)
            company.description = form.cleaned_data.get('description')
            company.address = form.cleaned_data.get('address')
            company.postal = form.cleaned_data.get('postal')
            company.city = form.cleaned_data.get('city')
            company.province = form.cleaned_data.get('province')
            fb = form.cleaned_data.get('fb_link')
            company.fb_link =fb
            company.twitter_link = form.cleaned_data.get('twitter_link')
            company.instagram_link = form.cleaned_data.get('instagram_link')
            company.save()
            
            return JsonResponse({'good':'We have saved your company information!'})
        else:
            print(form.errors)
            return JsonResponse({'errors':'Please double check your form. There may be errors.'})


def servicesDetailView(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        biz_name = BusinessName()
        context['business_registration_form'] = user_form
        return render(request, 'accountprod/bussignup.html', {'user_form':user_form,'biz_name':biz_name})
        
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))

    company = Company.objects.get(user=user)
    products = ProductModel.objects.filter(business=company)
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        services = paginator.page(1)
    except EmptyPage:
        services = paginator.page(paginator.num_pages)
    product_form = AddProductForm()
    servcategory_form = AddServiceCategoryForm(initial={'company':company})
    category_form = AddServiceToCategory(initial={'company':company})
    errors = False
    success = 'success'
    msg=''
    try:
        errormsg = request.session.get('formerror')
        if errormsg:
            success = 'danger'
            msg=errormsg
            errors = True
            del request.session['formerror']
    except:
        errormsg = None
    try:
        errormsg = request.session.get('formsuccess')
        if errormsg:
            success = 'success'
            msg=errormsg
            errors = True
            del request.session['formsuccess']
    except:
        errormsg = None
    return render(request,'productadmin/companydetail/services/products.html', {'errors':errors,'errormsg':msg,'success':success,'company':company, 'products':products, 'product_form':product_form, 'category_form':category_form,'servcategory_form':servcategory_form})

from itertools import chain

def clientListView(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        biz_name = BusinessName()
        context['business_registration_form'] = user_form
        return render(request, 'accountprod/bussignup.html', {'user_form':user_form,'biz_name':biz_name})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    
    company = Company.objects.get(user=user)
    clients = company.clients.all()
    form = AddClientForm()
    return render(request,'bizadmin/companydetail/client/clients.html', {'company':company, 'clients':clients, 'form':form})

from django import template

register = template.Library()

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)

@login_required
def reviewListView(request):
    if not request.user.is_authenticated:
        context={}
        user_form = BusinessRegistrationForm()
        biz_name = BusinessName()
        context['business_registration_form'] = user_form
        return render(request, 'accountprod/bussignup.html', {'user_form':user_form})
    email = request.user.email
    user = get_object_or_404(Account, email=email)
    if not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    
    company = Company.objects.get(user=user)
    reviews = Reviews.objects.filter(company=company)
    paginator = Paginator(reviews, 10)
    page = request.GET.get('page')
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    return render(request,'bizadmin/dashboard/reviews/reviews.html', {'page':page,'company':company, 'reviews':reviews})

class getBooking(View):
    def get(self, request):
        company = get_object_or_404(Company, user=request.user)
        booking_id = request.GET.get('booking_id')
        booking = Bookings.objects.get(id=booking_id)
        try:
            extra = bookingForm.objects.filter(booking=booking)
        except:
            extra = None
        service = booking.service
        if booking.user:
            user = booking.user
            htmlString = render_to_string('bizadmin/dashboard/schedule/bookingInfo.html',{'user':user, 'booking':booking, 'extra':extra, 'company':company})
            first_name = user.first_name
            last_name = user.last_name
        else:
            htmlString = render_to_string('bizadmin/dashboard/schedule/bookingInfo.html',{'user':booking.guest, 'booking':booking, 'extra':extra, 'company':company})
        return JsonResponse({'html_string':htmlString})

import celery
from celery import app
from django.core.exceptions import ObjectDoesNotExist



class changeDarkMode(View):
    def post(self, request):
        data=json.loads(request.body)
        light = data['light']
        company = Company.objects.get(user=request.user)
        if company.darkmode:
            company.darkmode = False
        else:
            company.darkmode = True
        company.save()
        return JsonResponse({'darkmode':company.darkmode})

from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
        

def dbrun(request):
    allcomp = Company.objects.all()

    for comp in allcomp:
        allbooking = comp.company_bookings.all()
        usr = comp.user
        staff = StaffMember.objects.get(user=usr)
        for booking in allbooking:
            if not booking.staffmem:
                booking.staffmem = staff
                booking.save()
            
    return JsonResponse({'':''})

class customThemeAPI(View):
    def post(self, request):
        user=request.user
        staff = StaffMember.objects.get(user=request.user)
        company = staff.company
        if staff.access == 2:
            bg = '.' + company.background + 'background'
            background = request.POST.get('background')
            message=''
            if background == 'primary':
                company.background = 'primary'
                newbg = '.primarybackground'
                message = 'The primary theme has been applied to your ecommerce page.'
            elif background == 'carbon':
                company.background = 'carbon'
                newbg = '.carbonbackground'
                message = 'The carbon theme has been applied to your ecommerce page.'
            elif background == 'lightblue':
                company.background = 'lightblue'
                newbg = '.lightbluebackground'
                message = 'The light blue theme has been applied to your ecommerce page.'
            else:
                company.background = 'hexagon'
                newbg = '.hexagonbackground'
                message = 'The hexagon theme has been applied to your ecommerce page.'
            company.save()
        return JsonResponse({'oldbackground':bg, 'newbackground':newbg, 'message':message})

class integrationZoomSignUp(View):
    def get(self, request):
        user = request.user
        return render(request, 'welcome/welcome.html', {'user':user, 'none':'d-none'})


class paymentsView(View):
    def get(self, request):
        company = get_object_or_404(Company, user=request.user)
        user=request.user
        staff = StaffMember.objects.get(user=user)
        payment_form = ServicePaymentCollectForm(initial={'collectpayment':staff.collectpayment, 'collectnrfpayment':staff.collectnrfpayment,'nrfpayment':staff.nrfpayment, 'currency':staff.currency})
        if user.is_business and not user.on_board:
            return redirect(reverse('completeprofile', host='prodadmin'))
        elif not user.is_business:
            loginViews(request)
        staff = StaffMember.objects.get(user=user)
        try:
            stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
            user_id = company.stripe_user_id_prod
            account_connected = stripe.Account.retrieve(user_id)
            if user_id=='':
                account_connected = False
        except Exception as e:
            account_connected = False
        return render(request,'productadmin/dashboard/account/payments.html', {'company':company, 'staff':staff, 'payment_form':payment_form, 'account_connected':account_connected})
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form

import stripe
from django.http import HttpResponseRedirect
class StripeAuthorizeView(View):
    def get(self, request):
        company = get_object_or_404(Company, user=request.user)
        user=request.user
        if user.is_business and not user.on_board:
            return redirect(reverse('completeprofile', host='prodadmin'))
        url = 'https://connect.stripe.com/oauth/authorize'
        if not settings.DEBUG:
            domainurl = f'https://biz.shopme.to/dashboard/profile/payments/oauth/callback'
        else:
            domainurl = f'http://biz.shopme.com:8000/dashboard/profile/payments/oauth/callback'
        params = {
            'response_type': 'code',
            'scope': 'read_write',
            'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
            'redirect_uri': domainurl
        }
        url = f'{url}?{urllib.parse.urlencode(params)}'
        return redirect(url)

class StripeAuthorizeCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        if code:
            data = {
                'client_secret': settings.STRIPE_SECRET_KEY,
                'grant_type': 'authorization_code',
                'client_id': settings.STRIPE_CONNECT_CLIENT_ID,
                'code': code
            }
            url = 'https://connect.stripe.com/oauth/token'
            resp = requests.post(url, params=data)
            stripe_user_id = resp.json()['stripe_user_id']
            stripe_access_token = resp.json()['access_token']
            company = Company.objects.get(user=request.user)
            company.stripe_access_token_prod = stripe_access_token
            company.stripe_user_id_prod = stripe_user_id
            company.save()
        url = reverse('staff_payments', host='prodadmin')
        response = redirect(url)
        return response

class StripeDeauthorizeView(View):
    def post(self, request):
        company = Company.objects.get(user=request.user)
        company.stripe_access_token_prod = ''
        company.stripe_user_id_prod = ''
        company.save()
        return JsonResponse({'response':''})

@login_required()
def completeSubscriptionPayment(request):
    company = get_object_or_404(Company, user=request.user)
    user=request.user
    staff = StaffMember.objects.get(user=user)
    stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
    try:
        subscription_id = company.stripe_subscription.id
        customer_id = company.stripe_customer.id
        subscription = stripe.Subscription.retrieve(subscription_id)
    except:
        return redirect(reverse('payments_to_bookme', host='prodadmin'))
    if subscription.status == 'active':
        company.subscriptionplan = 1
        company.save()
        return render(request, 'bizadmin/dashboard/account/monthlypayment/confirmationpage.html', {'company':company, 'staff':staff})
    else:
        return redirect(reverse('payments_to_bookme', host='prodadmin'))

from djstripe.models import Product
from businessadmin.decorators import log_exceptions
 
@log_exceptions('payMonthlyView')
@login_required
def payMonthlyView(request):
    company = get_object_or_404(Company, user=request.user)
    user=request.user
    staff = StaffMember.objects.get(user=user)
    if user.is_business and not user.on_board:
        return redirect(reverse('completeprofile', host='prodadmin'))
    products = Product.objects.all()
    stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
    pk = settings.STRIPE_PUBLISHABLE_KEY
    try:
        subscription_id = company.stripe_subscription.id
        customer_id = company.stripe_customer.id
        subscription = stripe.Subscription.retrieve(subscription_id)
        customer = stripe.Customer.retrieve(customer_id)
        paymentmethod_id = customer.invoice_settings.default_payment_method
        paymentmethod = stripe.PaymentMethod.retrieve(paymentmethod_id)
        cardbrand = paymentmethod.card.brand
        last4 = paymentmethod.card.last4
        if not subscription.status == 'active':
            return render(request,'bizadmin/dashboard/account/monthlypayment/pricing.html', {'company':company, 'staff':staff, 'products':products, 'pk_stripe':pk})
        # plan = subscription.items.data.product
    except:
        return render(request,'bizadmin/dashboard/account/monthlypayment/pricing.html', {'company':company, 'staff':staff, 'products':products, 'pk_stripe':pk})
    return render(request,'bizadmin/dashboard/account/monthlypayment/yourpayments.html', {'company':company, 'staff':staff, 'products':products, 'brand':cardbrand, 'last4':last4})

class webhook_received(View):
    def post(self, request):
        # You can use webhooks to receive information about asynchronous payment events.
        # For more about our webhook events check out https://stripe.com/docs/webhooks.
        webhook_secret = settings.WEBHOOK_SECRET_SUBSCRIPTION
        request_data = json.loads(request.data)

        if webhook_secret:
            # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
            signature = request.headers.get('stripe-signature')
            try:
                event = stripe.Webhook.construct_event(
                    payload=request.data, sig_header=signature, secret=webhook_secret)
                data = event['data']
            except Exception as e:
                return e
            # Get the type of webhook event sent - used to check the status of PaymentIntents.
            event_type = event['type']
        else:
            data = request_data['data']
            event_type = request_data['type']

        data_object = data['object']

        if event_type == 'invoice.paid':
            # Used to provision services after the trial has ended.
            # The status of the invoice will show up as paid. Store the status in your
            # database to reference when a user accesses your service to avoid hitting rate
            # limits.
            print(data)

        if event_type == 'invoice.payment_failed':
            # If the payment fails or the customer does not have a valid payment method,
            # an invoice.payment_failed event is sent, the subscription becomes past_due.
            # Use this webhook to notify your user that their payment has
            # failed and to retrieve new card details.
            print(data)

        if event_type == 'customer.subscription.deleted':
            # handle subscription cancelled automatically based
            # upon your subscription settings. Or if the user cancels it.
            print(data)

        return jsonify({'status': 'success'})