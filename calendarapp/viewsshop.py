from django.shortcuts import render, get_object_or_404, redirect
from account.models import Account
from account.forms import ConsumerRegistrationForm
from business.models import Company, Services, OpeningHours, Clients, CompanyReq, Gallary, Category, SubCategory, Amenities
from businessadmin.models import StaffWorkingHours, StaffMember, Breaks
from consumer.models import Bookings, extraInformation, Reviews
from .models import bookingForm
from django.db.models import Count
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
from products.models import Product
from django_hosts.resolvers import reverse

class ProductDetails(View):
    def get(self, request, slug):
        user = request.user
        company = request.viewing_company
        if company.business_type == 'service':
            return redirect(reverse('bookingurls', host='bookingurl', host_args=(company.slug,)))
        product = Product.objects.get(business=company, slug=slug)
        return render(request, 'productspage/details/productdetail.html',{'user':user,'company':company, 'product':product})


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
