from django.conf.urls import url, include

from . import views
app_name = 'businessadmin'
urlpatterns = [
    url(r'admin/schedule/$', views.scheduleView, name='schedule'),
    url(r'admin/profile/security/$',views.profileSecurityViews, name='security'),
    url(r'admin/profile/billing/$',views.profileBillingViews, name='billing'),
    url(r'admin/profile/$',views.profileViews, name='profile'),
    url(r'signup/$', views.signupViews, name='bizadminsignup'),
    url(r'login/$', views.loginViews, name='bizadminlogin'),
    url(r'^faq/$', views.faqBusinessViews, name='faqbusiness'),
    url(r'^pricing/$', views.pricingViews, name='pricingBusiness'),
    url(r'^$', views.businessadmin, name='bizadminmain'),
]