from django.conf.urls import url, include
from django.urls import path, re_path
from . import views
app_name = 'products'
urlpatterns = [
    path('cancel/', views.payment_cancel, name='cancel'),
    path('processed/', views.requires_capture, name='capture'),
    path('completed/', views.payment_done, name='done'),
    path('load/states/', views.loadStates, name='loadstate'),
    path('complete/', views.commitPurchase.as_view(), name='commitpurchase'),
    path('paymentprocessing/', views.PaymentProcessingProducts.as_view(), name='newpaymentprocessing'),
    path('shipping/',views.ShippingView.as_view(), name='cart_shippingcalc'),
    path('checkout/',views.CartCheckoutView.as_view(), name='cart_checkout'),
    path('cartaddproduct/<int:product_id>/', views.cart_add, name='cart_add_product'),
    path('retrievefilteredsearchproduct/', views.SearchFilter.as_view(), name='productsearch'),
    path('<slug:slug>/', views.ProductDetails.as_view(), name='productdetail'),
    # path('', views.product_list, name='list'),
    path('', views.ProductMain.as_view(), name='productmain'),
    
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)