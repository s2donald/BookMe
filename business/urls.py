from django.urls import path
from . import views
app_name = 'business'
urlpatterns = [
    path('services/', views.ManageServiceListView,name='manage_service_list'),
    path('create/', views.CreateServiceView, name='create_service'),
    path('delete/<int:pk>/', views.DeleteServiceView, name='delete_service'),
    path('update/<int:pk>/', views.UpdateServiceView, name='update_service'),
    path('<slug:slug>/<int:id>/',views.company_detail,name='company_detail'),
    path('<slug:category_slug>/',views.company_list, name='company_list_by_category'),
    path('list/', views.company_list, name='company_list'),
    path('', views.homepage, name='homepage'),
    
]