from django.conf.urls import url, include

from . import views
app_name = 'businessadmin'
urlpatterns = [
    url(r'bpage/hours/$', views.businessHoursView, name='hours'),
    url(r'bpage/photo/$', views.businessPhotoView, name='photos'),
    url(r'bpage/amentities/$', views.businessAmenitiesView, name='amenities'),

    url(r'dashboard/schedule/$', views.scheduleView, name='schedule'),
    url(r'dashboard/profile/booking/$', views.bookingSettingViews, name='bookingSetting'),
    url(r'dashboard/profile/security/$',views.profileSecurityViews, name='security'),
    url(r'dashboard/profile/notifs/$', views.notifViews, name='notifications'),
    url(r'dashboard/profile/billing/$',views.profileBillingViews, name='billing'),
    url(r'dashboard/profile/$',views.profileViews, name='profile'),
    url(r'updateBookingInterval/$', views.bookingAPI.as_view() ,name='bookingIntervalAPI'),
    url(r'returningbookingReturningAPI/$', views.returningAPI.as_view(), name='bookingReturningAPI'),

    url(r'update/emailinfo/$', views.updateEmailSetting.as_view(), name='emailUpdate'),
    url(r'update/notes/$', views.notesUpdate.as_view(), name='notesUpdate'),

    url(r'delete/booking/$', views.deleteBookingAPI.as_view(), name='delete_booking'),

    url(r'detail/info/$', views.compinfoViews, name='information'),
    url(r'detail/service/$', views.servicesDetailView, name='service_detail'),
    url(r'detail/clients/$', views.clientListView, name='client_list'),

    url(r'creating/$', views.createserviceViews, name='service_create'),
    url(r'delete/(?P<pk>\d+)/$', views.deleteserviceViews, name='service_delete'),
    url(r'update/(?P<pk>\d+)/$', views.updateserviceViews, name='service_update'),

    url(r'creatings/$', views.createserviceAPI.as_view(), name='createservice'),
    url(r'deletes/(?P<pk>\d+)/$', views.deleteserviceAPI.as_view(), name='deleteservice'),
    url(r'updates/(?P<pk>\d+)/$', views.updateserviceAPI.as_view(), name='updateservice'),

    url(r'creatingc/$', views.createclientAPI.as_view(), name='createclient'),
    url(r'deletec/(?P<pk>\d+)$', views.deleteclientAPI.as_view(), name='deleteclient'),
    url(r'updatec/(?P<pk>\d+)/$', views.updateclientAPI.as_view(), name='updateclient'),

    url(r'reviews/$', views.reviewListView, name='reviewlist'),
    url(r'privatetoggle/$', views.changePrivateView.as_view(), name='changePrivate'),

    url(r'path/loadsubcategories', views.load_subcat, name='ajax_load_subcategories'),
    url(r'onboarding/check/subdomain/$', views.subdomainCheck.as_view(), name='subdomain'),
    url(r'onboarding/$', views.completeViews, name='completeprofile'),
    url(r'^updatecompanyform/$',views.updateCompanyDetail.as_view(), name='updateform'),
    url(r'^companyformsave/$', views.saveCompanyDetail.as_view(), name='saveDetailForm'),
    url(r'^accountFormSave/$', views.personDetailSave.as_view(), name='accountCheck'),
    url(r'home/$', views.homepageViews, name='home'),

    url(r'getbook/$', views.getBooking.as_view(), name='getBookingId'),

    url(r'deletegal/$', views.deleteGalPic.as_view(), name='deletegalpic'),
    url(r'galupload/$', views.galImageUpload, name='galleryupload'),
    url(r'imageuploads/$', views.headerImageUploads, name='imageuploads'),
    url(r'imageupload/$', views.headerImageUpload, name='imageupload'),
    url(r'profileimg/$', views.profileImageUpload, name='profileimg'),
    url(r'file-upload/$', views.fileUploadView, name='upload'),

    url(r'createbusiness/$', views.createNewBusiness, name='newbizcreate'),
    url(r'signup/$', views.signupViews, name='bizadminsignup'),
    url(r'logout/$', views.LogoutView, name='bizadminlogout'),
    url(r'login/$', views.loginViews, name='bizadminlogin'),

    url(r'^faq/$', views.faqBusinessViews, name='faqbusiness'),

    url(r'requests/', views.requestListViews, name='requestList'),
    url(r'requestedAdd/(?P<pk>\d+)/$', views.addRequestedViews.as_view(), name='addRequested'),
    url(r'requestedDelete/(?P<pk>\d+)/$', views.deleteRequestedViews.as_view(), name='deleteRequested'),

    url(r'^addamenity/$', views.addAmenityAPI.as_view(), name='addamenity'),
    url(r'^removeamenity/$', views.removeAmenityAPI.as_view(), name='removeamenity'),
    url(r'^addtag/$', views.addTagAPI.as_view(), name='addtag'),
    url(r'^removetag/$', views.removeTagAPI.as_view(), name='removetag'),
    url(r'^addbusinessh/$',views.saveBusinessHours.as_view(), name='businessHourSave'),


    url(r'^updatedpass/$', views.updatePassword.as_view(), name='updatepassword'),
    url(r'^pricing/$', views.pricingViews, name='pricingBusiness'),
    url(r'^$', views.businessadmin, name='bizadminmain'),

]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)