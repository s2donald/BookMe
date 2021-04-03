from django.conf.urls import url, include
from django.urls import path, re_path
from . import views
app_name = 'products'
urlpatterns = [
    path('<slug:slug>/',viewsshop.ProductDetails.as_view(), name='productdetail'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)