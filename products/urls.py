from django.conf.urls import url, include
from django.urls import path, re_path
from . import views
app_name = 'products'
urlpatterns = [
    path('cartaddproduct/<int:product_id>/', views.cart_add, name='cart_add_product'),
    path('retrievefilteredsearchproduct/', views.SearchFilter.as_view(), name='productsearch'),
    path('<slug:slug>/', views.ProductDetails.as_view(), name='productdetail'),
    path('', views.ProductMain.as_view(), name='productmain')
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)