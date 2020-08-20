from django.shortcuts import render, get_object_or_404
from business.models import Company, Services
# Create your views here.


def get_companyslug(request, slug):
    request.viewing_company = get_object_or_404(Company, slug=slug)

def bookingurl(request):
    user = request.user
    company = request.viewing_company
    services = Services.objects.filter(business=company)
    return render(request, 'bookingpage/bookingpage.html', {'user': user, 'company':company, 'services':services})

def bizadmin(request):
    user = request.user
    return render(request, 'businessadmin/bizadmin.html', {'user': user})