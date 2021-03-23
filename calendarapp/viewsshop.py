from django.shortcuts import render, get_object_or_404
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

