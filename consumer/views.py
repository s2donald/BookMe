from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from business.models import Company, SubCategory, Category
from .models import Bookings
# from datetime import datetime
from django.utils import timezone
from business.forms import SearchForm
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

@login_required
def FutPastBooking(request):
    today = timezone.now()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    futureBookings = Bookings.objects.filter(user=request.user, end__gt=today)
    pastBookings = Bookings.objects.filter(user=request.user, end__lte=today).order_by('-end')
    
    paginator = Paginator(futureBookings, 3)
    page = request.GET.get('page')
    try:
        futureBookings = paginator.page(page)
    except PageNotAnInteger:
        futureBookings = paginator.page(1)
    except EmptyPage:
        futureBookings = paginator.page(paginator.num_pages)

    paginator = Paginator(pastBookings, 3)
    page = request.GET.get('pagepast')
    try:
        pastBookings = paginator.page(page)
    except PageNotAnInteger:
        pastBookings = paginator.page(1)
    except EmptyPage:
        pastBookings = paginator.page(paginator.num_pages)

    form = SearchForm()
    return render(request, 'account/bookingsched.html',{'page':page,'pastBookings':pastBookings,'futureBookings':futureBookings,'today':today,'categories':categories,'subcategories':subcategories,'form':form})

