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
from gibele import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.loader import render_to_string
import multiprocessing
from dateutil.relativedelta import relativedelta
from django.contrib.postgres.search import TrigramSimilarity
from products.models import Product, addOnProducts, MainProductDropDown, ProductDropDown
from products.cart import ProductCart
from django_hosts.resolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ProductMain(View):
    @xframe_options_exempt
    def get(self, request):
        user = request.user
        company = request.viewing_company
        dateWindowBefore = timezone.localtime(timezone.now()) + datetime.timedelta(days=company.before_window_day,hours=company.before_window_hour,minutes=company.before_window_min)
        dateWindowAfter = timezone.localtime(timezone.now()) + relativedelta(days=company.after_window_day,months=company.after_window_month)
        kanalytics = request.GET.get('k')
        return render(request, 'productspage/productpage.html',{'user':user,'company':company, 'dateWindowBefore':dateWindowBefore, 'dateWindowAfter':dateWindowAfter})

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
            products = Product.objects.annotate(similarity=TrigramSimilarity('name', Search),).filter(similarity__gt=0.3, business=company).order_by('-similarity')
        html = render_to_string('productspage/details/partial_search/partialproductsearch.html', {'company':company, 'products':products}, request)
        return JsonResponse({'html_content':html})



# Create your views here.
from django.contrib.admin.utils import flatten
@require_POST
def cart_add(request, product_id):
    cart = ProductCart(request)
    user = request.user
    company = request.viewing_company
    # print(request.POST)
    addon_options = request.POST.getlist('addon_options')
    product = get_object_or_404(Product, id=product_id)
    product_addons = addOnProducts.objects.filter(id__in=addon_options)
    dropdownaddons = []
    for dropdowns in product.product_maindropdown.all():
        option = request.POST.getlist('addon_dropdown_'+str(dropdowns.id))
        if len(option) > 0:
            dropdownaddons.append(option)
    drrop = ProductDropDown.objects.filter(id__in=flatten(dropdownaddons))
    cart.add(product=product, addon_list=flatten(addon_options), dropdown_list=flatten(dropdownaddons), prod_addon=product_addons, dropdown_addon=drrop, quantity=1, override_quantity=True)
    # print(cart.clear())
    # print(cart.get_total_price())
    return redirect(reverse('cart_checkout', host='producturl', host_args=(company.slug,)))


class CartCheckoutView(View):
    def get(self, request):
        user = request.user
        company = request.viewing_company
        cart = ProductCart(request)
        
        # addon_options = request.GET.getlist('addon_options')
        # product = get_object_or_404(Product, id=product_id)
        # dropdownaddons = []
        # for dropdowns in product.product_maindropdown.all():
        #     option = request.GET.getlist('addon_dropdown_'+str(dropdowns.id))
        #     if len(option) > 0:
        #         dropdownaddons.append(option)
        
        # print(addon_options)
        # print()
        # print(product)
        # print()
        # print(dropdownaddons)
        return render(request, 'productspage/details/productcheckout.html',{'user':user,'company':company, 'cart':cart})