from django.shortcuts import render

# Create your views here.

def businessadmin(request):
    return render(request, 'welcome/welcome.html')

def pricingViews(request):
    return render(request, 'welcome/pricing.html')

def faqBusinessViews(request):
    return render(request, 'welcome/faq.html')