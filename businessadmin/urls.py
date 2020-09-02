from django.conf.urls import url, include

from . import views
app_name = 'businessadmin'
urlpatterns = [
    url(r'admins/schedule/$', views.scheduleView, name='schedule'),
    url(r'admins/profile/security/$',views.profileSecurityViews, name='security'),
    url(r'admins/profile/billing/$',views.profileBillingViews, name='billing'),
    url(r'admins/profile/$',views.profileViews, name='profile'),
    url(r'signup/$', views.signupViews, name='bizadminsignup'),
    url(r'login/$', views.loginViews, name='bizadminlogin'),
    url(r'^faq/$', views.faqBusinessViews, name='faqbusiness'),
    url(r'^pricing/$', views.pricingViews, name='pricingBusiness'),
    url(r'^$', views.businessadmin, name='bizadminmain'),
]