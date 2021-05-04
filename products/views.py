from django.shortcuts import render, get_object_or_404, redirect
from account.models import Account
from account.forms import ConsumerRegistrationForm
from business.models import Company, Services, OpeningHours, Clients, CompanyReq, Gallary, Category, SubCategory, Amenities
from businessadmin.models import StaffWorkingHours, StaffMember, Breaks
from consumer.models import Bookings, extraInformation, Reviews
from calendarapp.models import bookingForm
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
import json, urllib
from django.core import serializers
import datetime, pytz
from django.utils import timezone
from account.forms import UpdatePersonalForm, AccountAuthenticationForm, AccountAuthenticationFormId,GuestPersonalForm
from django.contrib.auth import authenticate, login
from django.core.validators import validate_email
from django import forms
from account.tasks import reminderEmail, emailRequestServiceCompany, confirmedEmail, consumerCreatedEmailSent, confirmedEmailCompany, send_sms_reminder_client, send_sms_confirmed_client, emailRequestServiceClient, send_sms_requestService_company, send_sms_requestService_client
from businessadmin.tasks import requestToBeClient
from business.forms import VehicleMakeModelForm, AddressForm
import re
from .tasks import order_payment_completed
from gibele import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.loader import render_to_string
import multiprocessing
from dateutil.relativedelta import relativedelta
from django.contrib.postgres.search import TrigramSimilarity
from products.models import Product, MainProductDropDown, ProductDropDown, Order, OrderItem, QuestionModels, AnswerModels, MultipleImageOrderAttachments
from products.cart import ProductCart
from django_hosts.resolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import stripe, djstripe
from .forms import OrderCreateForm
from django.http import HttpResponse
class ProductMain(View):
    @xframe_options_exempt
    def get(self, request):
        user = request.user
        company = request.viewing_company
        dateWindowBefore = timezone.localtime(timezone.now()) + datetime.timedelta(days=company.before_window_day,hours=company.before_window_hour,minutes=company.before_window_min)
        dateWindowAfter = timezone.localtime(timezone.now()) + relativedelta(days=company.after_window_day,months=company.after_window_month)
        kanalytics = request.GET.get('k')
        Search = request.GET.get('search_query')
        if Search is None or Search == '':
            products = company.products_offered.all()
        else:
            products = Product.objects.annotate(similarity=TrigramSimilarity('name', Search),).filter(similarity__gt=0.08, business=company).order_by('-similarity')
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            # if request.is_ajax():
            #     return HttpResponse('')
            products = paginator.page(paginator.num_pages)
        # if request.is_ajax():
        #     return render(request, 'productspage/details/partial_search/partial_list.html', {'company':company, 'products':products})
        return render(request, 'productspage/productpage.html',{'user':user,'company':company,'products':products, 'search':Search})

def product_list(request):
    company = request.viewing_company
    products = company.products_offered.all()
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        products = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'productspage/details/partial_search/partialproductsearch.html', {'company':company, 'products':products})

class ProductDetails(View):
    def get(self, request, slug):
        user = request.user
        company = request.viewing_company
        # if company.business_type == 'service':
        #     return redirect(reverse('bookingurls', host='bookingurl', host_args=(company.slug,)))
        product = Product.objects.get(business=company, slug=slug)
        reviews = product.product_reviews.all()
        paginator = Paginator(reviews, 15)
        page = request.GET.get('page')
        try:
            reviews = paginator.page(page)
        except PageNotAnInteger:
            reviews = paginator.page(1)
        except EmptyPage:
            reviews = paginator.page(paginator.num_pages)
        return render(request, 'productspage/details/productdetail.html',{'user':user,'company':company, 'product':product, 'page':page, 'reviews':reviews})

class SearchFilter(View):
    def get(self, request):
        company = request.viewing_company
        Search = request.GET.get('search_query')
        if Search == '':
            products = Product.objects.filter(business=company)
        else:
            products = Product.objects.annotate(similarity=TrigramSimilarity('name', Search),).filter(similarity__gt=0.08, business=company).order_by('-similarity')
        html = render_to_string('productspage/details/partial_search/partialproductsearch.html', {'company':company, 'products':products}, request)
        return JsonResponse({'html_content':html})



# Create your views here.
from django.contrib.admin.utils import flatten
@require_POST
def cart_add(request, product_id):
    cart = ProductCart(request)
    user = request.user
    company = request.viewing_company
    product = get_object_or_404(Product, id=product_id)
    dropdownaddons = []
    for dropdowns in product.product_maindropdown.all():
        option = request.POST.getlist('addon_dropdown_'+str(dropdowns.id))
        if len(option) > 0:
            dropdownaddons.append(option)
    drrop = ProductDropDown.objects.filter(id__in=flatten(dropdownaddons))
    cart.add(product=product, dropdown_list=flatten(dropdownaddons), dropdown_addon=drrop, quantity=1, override_quantity=True)
    # print(cart.clear())
    # print(cart.get_total_price())
    return redirect(reverse('cart_checkout', host='producturl', host_args=(company.slug,)))


class CartCheckoutView(View):
    def get(self, request):
        user = request.user
        company = request.viewing_company
        cart = ProductCart(request)
        if len(cart)==0:
            return redirect(reverse('productmain', host='producturl', host_args=(company.slug,)))
        for item in cart:
            if item['company'] != company:
                cart.clear()
                return redirect(reverse('productmain', host='producturl', host_args=(company.slug,)))
        pk = settings.STRIPE_PUBLISHABLE_KEY
        form = OrderCreateForm()

        return render(request, 'productspage/details/productcheckout.html',{'form':form,'user':user,'company':company, 'cart':cart, 'pk_stripe':pk})

    def post(self, request):
        form = OrderCreateForm(request.POST)
        user = request.user
        company = request.viewing_company
        cart = ProductCart(request)
        pk = settings.STRIPE_PUBLISHABLE_KEY
        cart = ProductCart(request)
        if form.is_valid():
            order = form.save(commit=False)
            order.company = company
            total = cart.get_total_price()
            order.save()
            for item in cart:
                dropdowns=item['dropdownoptions']
                product = item['product']
                orditems = OrderItem.objects.create(order=order,
                                        company=item['company'],
                                        product=product,
                                        price=total,
                                        quantity=1
                                    )
                if product.request:
                    order.pendingapproval = True
                else:
                    order.pendingapproval = False
                order.company = item['company']
                order.active = True
                if product.dispatch != 0:
                    order.dateshipped = timezone.localtime(timezone.now()) + datetime.timedelta(days=product.dispatch)
                order.delivered = False
                order.save()
                for drop in dropdowns:
                    orditems.dropdown.add(drop)
                for additional in product.product_questions.all():
                    q = QuestionModels.objects.get(pk=str(additional.id))
                    description = ''
                    img = None
                    if q.retrievetype == 0:
                        description = request.POST.get(str(additional.id))
                    else:
                        img = request.FILES.get(str(additional.id))
                        print(request.FILES)
                    answer = AnswerModels.objects.create(orderitem=orditems,question=q,description=description)
                    if img:
                        MultipleImageOrderAttachments.objects.create(answer=answer,photos=img,orderitem=orditems)
                        


            cart.clear()
            request.session['order_id'] = order.id
            return redirect(reverse('newpaymentprocessing', host='producturl', host_args=(company.slug,)))
        else:
            return render(request, 'productspage/details/productcheckout.html',{'form':form,'user':user,'company':company, 'cart':cart, 'pk_stripe':pk})

class PaymentProcessingProducts(View):
    def get(self, request):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        company = request.viewing_company
        total_cost = order.get_total_cost()
        pk = settings.STRIPE_PUBLISHABLE_KEY
        enabled = True
        for item in order.items.all():
            if item.company != company:
                return redirect(reverse('productmain', host='producturl', host_args=(company.slug,)))
        if company.stripe_access_token_prod is None or company.stripe_user_id_prod is None:
            enabled = False
        return render(request, 'productspage/details/purchaseproduct.html',{'order':order, 'pk_stripe':pk, 'company':company, 'enabled':enabled})
    def post(self, request):
        data = json.loads(request.body)
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        payment_method = data['payment_method']
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)
        cart = ProductCart(request)
        
        company = order.company
        payment_method_obj = stripe.PaymentMethod.create(
            payment_method=payment_method,
            stripe_account=company.stripe_user_id_prod,
        )
        total = order.get_total_cost()
        price = (float(total) * 100)
        applicationfee = (float(total) * 3) + 10
        try:
            payment_intent = stripe.PaymentIntent.create(
                payment_method_types=['card'],
                amount=round(price),
                # customer=customer.id,
                currency='cad',
                application_fee_amount=round(applicationfee),
                stripe_account=company.stripe_user_id_prod,
                capture_method = 'manual',
                confirm=True,
                payment_method=payment_method_obj
            )
            payment_intent['stripe_staff_account_id'] = company.stripe_user_id_prod
            request.session['payment_intent_id'] = payment_intent.id
            # print(subscription.latest_invoice.payment_intent)
            return JsonResponse(payment_intent)
        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status =403)

from cities.models import City, Region
def loadStates(request):
    company = request.viewing_company
    country_id = request.GET.get('country')
    if country_id:
        states = Region.objects.filter(country__code=country_id).order_by('name')
    else:
        states = None
    return render(request, 'productspage/details/partial_search/partial_states.html', {'countries': states})

class commitPurchase(View):
    def get(self, request):
        return render(request, 'payment/done.html')
    def post(self, request):
        company = request.viewing_company
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY
        payment_intent_id = request.session.get('payment_intent_id')
        if payment_intent_id:
            is_request = False
            for item in order.items.all():
                if item.product.request:
                    is_request = True
            if not is_request:
                stripe.PaymentIntent.capture(
                    payment_intent_id,
                    stripe_account=company.stripe_user_id_prod
                )
            payintent = stripe.PaymentIntent.retrieve(
                payment_intent_id,
                stripe_account=company.stripe_user_id_prod
            )
            if payintent.status == 'succeeded':
                order.paid = True
                order.orderplaced = True
                order.pendingapproval = False
                order.paymentintent = payment_intent_id
                order.save()
                order_payment_completed.delay(order_id)
                return redirect(reverse('done', host='producturl', host_args=(company.slug,)))
            elif payintent.status == 'requires_capture':
                order.orderplaced = True
                order.paymentintent = payment_intent_id
                order.save()
                order_payment_completed.delay(order_id)
                return redirect(reverse('capture', host='producturl', host_args=(company.slug,)))
        return redirect(reverse('cancel', host='producturl', host_args=(company.slug,)))

def payment_done(request):
    company = request.viewing_company
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'productspage/details/puchase_complete.html', {'company':company, 'order':order})

def requires_capture(request):
    company = request.viewing_company
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'productspage/details/requires_capture.html', {'company':company, 'order':order})

def payment_cancel(request):
    return render(request, 'productspage/details/puchase_canceled.html')