from django.shortcuts import render

# Create your views here.

def businessadmin(request):
    return render(request, 'welcome/welcome.html')

def pricingViews(request):
    return render(request, 'welcome/pricing.html')

def faqBusinessViews(request):
    return render(request, 'welcome/faq.html')


def signupViews(request):
    return render(request, 'account/bussignup.html')

def loginViews(request):
    return render(request, 'account/buslogin.html')