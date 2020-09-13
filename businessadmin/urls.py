from django.conf.urls import url, include

from . import views
app_name = 'businessadmin'
urlpatterns = [
    url(r'dashboard/schedule/$', views.scheduleView, name='schedule'),
    url(r'dashboard/profile/security/$',views.profileSecurityViews, name='security'),
    url(r'dashboard/profile/billing/$',views.profileBillingViews, name='billing'),
    url(r'dashboard/profile/$',views.profileViews, name='profile'),
    url(r'creating/$', views.createserviceViews, name='service_create'),
    url(r'delete/(?P<pk>\d+)/$', views.deleteserviceViews, name='service_delete'),
    url(r'update/(?P<pk>\d+)/$', views.updateserviceViews, name='service_update'),
    url(r'onboarding/check/subdomain/$', views.subdomainCheck.as_view(), name='subdomain'),
    url(r'onboarding/$', views.completeViews, name='completeprofile'),
    url(r'home/$', views.homepageViews, name='home'),
    url(r'file-upload/$', views.fileUploadView, name='upload'),
    url(r'signup/$', views.signupViews, name='bizadminsignup'),
    url(r'logout/$', views.LogoutView, name='bizadminlogout'),
    url(r'login/$', views.loginViews, name='bizadminlogin'),
    url(r'^faq/$', views.faqBusinessViews, name='faqbusiness'),
    url(r'^pricing/$', views.pricingViews, name='pricingBusiness'),
    url(r'^$', views.businessadmin, name='bizadminmain'),
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)