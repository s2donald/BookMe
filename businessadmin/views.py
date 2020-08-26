from django.shortcuts import render

# Create your views here.

def businessadmin(request):
    return render(request, 'welcome/main.html')