from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from business.models import Company, SubCategory, Category
from .models import Bookings
from datetime import datetime
from business.forms import SearchForm
from django.http import JsonResponse

# Create your views here.

@login_required
def FutPastBooking(request):
    today = datetime.today()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    futureBookings = Bookings.objects.filter(user=request.user, end__gt=today)
    pastBookings = Bookings.objects.filter(user=request.user, end__lte=today)
    my_companies = Company.objects.filter(user=request.user)
    form = SearchForm()
    return render(request, 'account/bookingsched.html',{'pastBookings':pastBookings,'futureBookings':futureBookings,'today':today,'categories':categories,'subcategories':subcategories,'my_companies':my_companies,'form':form})

