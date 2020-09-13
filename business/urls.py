from django.urls import path
from . import views
app_name = 'business'
urlpatterns = [
    path('services/<int:id>/<slug:slug>/', views.ManageServiceListView,name='manage_service_list'),
    path('create/<int:pk>/<slug:slug>/', views.CreateServiceView, name='create_service'),
    path('delete/<int:pk>/<int:pks>/<slug:slug>/', views.DeleteServiceView, name='delete_service'),
    path('update/<int:pk>/<int:pks>/<slug:slug>/', views.UpdateServiceView, name='update_service'),
    path('<slug:slug>/<int:id>/',views.company_detail,name='company_detail'),
    path('<slug:category_slug>/',views.company_list, name='company_list_by_category'),
    path('list/', views.company_list, name='company_list'),
    path('privacy/', views.privacyViews, name='privacy'),
    path('search', views.allsearch,name='post-search'),
    path('homesearch', views.homesearch,name='all-search'),
    path('', views.homepage, name='homepage'),
    
]