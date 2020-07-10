from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Company, Services
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from .forms import SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
def homepage(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    form = SearchForm()
    Search = None
    results = []
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            results = Company.objects.annotate(search=SearchVector('user','description'),).filter(search=Search)
            return render(request, 'business/company/list.html',{'category':category, 'categories':categories ,'companies':results})
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
    return render(request, 'business/home.html', {'category':category, 'categories':categories, 'form':form})

def company_list(request, category_slug=None, company_slug=None, tag_slug=None):
    category = None
    categories = Category.objects.all()
    companies = Company.objects.all()
    tag=None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        companies = companies.filter(category=category)
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        companies = companies.filter(tags__in=[tag])
    form = SearchForm()
    Search = None
    results = []
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            results = Company.objects.annotate(search=SearchVector('user','description'),).filter(search=Search)
            return render(request, 'business/company/list.html',{'category':category, 'categories':categories ,'companies':results})
    counts = companies.count()%6
    paginator = Paginator(companies, 4)
    page = request.GET.get('page')
    try:
        companiess = paginator.page(page)
    except PageNotAnInteger:
        companiess = paginator.page(1)
    except EmptyPage:
        companiess = paginator.page(paginator.num_pages)
    return render(request, 'business/company/list.html',{'page':page,'category':category, 'companies':companiess, 'categories':categories, 'counts':counts, 'form':form,'tag':tag})

def company_detail(request, id, slug):
    company = get_object_or_404(Company, id=id, slug=slug, available=True)
    category = None
    categories = Category.objects.all()
    services = Services.objects.all().filter(business=company)
    form = SearchForm()
    Search = None
    results = []
    if 'Search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            Search = form.cleaned_data['Search']
            results = Company.objects.annotate(search=SearchVector('user','description'),).filter(search=Search)
            return render(request, 'business/company/list.html',{'category':category, 'categories':categories ,'companies':results})
    return render(request, 'business/company/detail.html', {'company':company,'category':category,'categories':categories, 'services':services, 'form':form})

class BusinessMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(business=self.request.user)

class BusinessEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class BusinessServiceMixin(BusinessMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Services
    fields = ['name', 'description', 'business' ,'slug','price']
    success_url = reverse_lazy('manage_service_list')

class BusinessServiceEditMixin(BusinessServiceMixin, BusinessEditMixin):
    template_name = 'business/company/manage/service/form.html'

#Lists all the services that the business owner(user) has created. 
class ManageServiceListView(BusinessServiceMixin, ListView):
    template_name = 'business/company/manage/service/list.html'
    permission_required = 'business.view_service'

class ServiceCreateView(BusinessServiceEditMixin, CreateView):
    permission_required = 'business.add_service'

class ServiceUpdateView(BusinessServiceEditMixin, UpdateView):
    permission_required = 'business.change_service'

class ServiceDeleteView(BusinessServiceEditMixin, DeleteView):
    template_name = 'business/company/manage/service/delete.html'
    permission_required = 'business.delete_service'