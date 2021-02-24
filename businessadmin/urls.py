from django.conf.urls import url, include
from django.contrib import admin
from django.urls import re_path, path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'businessadmin'
urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('adminpagefordjangosuuwoop/', admin.site.urls),
    # re_path(r'databaserun/$', views.dbrun, name='dbrun'),

    re_path(r'businesspage/photo/$', views.businessPhotoView, name='photos'),
    re_path(r'businesspage/amentities/$', views.businessAmenitiesView, name='amenities'),
    re_path(r'businesspage/customization/$', views.businessPageCustomization, name='bpagecustomization'),
    re_path(r'api/addcustomize/theme/$', views.customThemeAPI.as_view(), name='toggletheme'),
    re_path(r'api/addnewformfield/$', views.addNewFormFieldAPI.as_view(), name='addnewformfield'),
    re_path(r'api/togglepath/$', views.toggleformrequiredAPI.as_view(), name='toggleformrequired'),
    re_path(r'api/editformfield/$', views.editFormFieldAPI.as_view(), name='editformrequired'),

    

    re_path(r'dashboard/schedule/$', views.scheduleView, name='schedule'),
    re_path(r'dashboard/profile/booking/$', views.bookingSettingViews, name='bookingSetting'),
    re_path(r'dashboard/profile/security/$',views.profileSecurityViews, name='security'),
    re_path(r'dashboard/profile/notifs/$', views.notifViews, name='notifications'),
    re_path(r'dashboard/profile/billing/$',views.profileBillingViews, name='billing'),
    re_path(r'dashboard/profile/$',views.profileViews, name='profile'),
    re_path(r'updateBookingInterval/$', views.bookingAPI.as_view() ,name='bookingIntervalAPI'),
    re_path(r'returningbookingReturningAPI/$', views.returningAPI.as_view(), name='bookingReturningAPI'),

    re_path(r'update/emailinfo/$', views.updateEmailSetting.as_view(), name='emailUpdate'),
    re_path(r'update/notes/$', views.notesUpdate.as_view(), name='notesUpdate'),

    re_path(r'delete/booking/$', views.deleteBookingByCompAPI.as_view(), name='delete_booking'),

    re_path('darkmode/', views.changeDarkMode.as_view(), name='changeDarkMode'),

    re_path(r'detail/info/$', views.compinfoViews, name='information'),
    re_path(r'detail/service/$', views.servicesDetailView, name='service_detail'),
    re_path(r'get/getstaffservice/', views.staffServicesViews.as_view(), name='getstaffservice'),
    re_path(r'post/addstaffservice/', views.addstaffServicesViews.as_view(), name='addstaffservice'),
    re_path(r'post/removestaffservice/', views.removestaffServicesViews.as_view(), name='removestaffservice'),
    re_path(r'post/addstaffworkinghours/', views.addstaffWorkingDaysViews.as_view(), name='addstaffworkingday'),
    re_path(r'post/savestaffworkinghours/', views.savestaffWorkingDaysViews.as_view(), name='savestaffworkingday'),
    re_path(r'post/savestaffbreakhours/', views.savestaffBreakDaysViews.as_view(), name='savestaffbreakday'),
    re_path(r'post/removestaffworkinghours/', views.removestaffWorkingDaysViews.as_view(), name='removestaffworkingday'),
    re_path(r'post/removestaffCompany/', views.removestaffCompany.as_view(), name='removestaffromcompany'),
    re_path(r'post/addbreakday/', views.addbreakdayViews.as_view(), name='addbreakday'),
    re_path(r'post/removebreakday/', views.removebreakdayViews.as_view(), name='removebreakday'),


    re_path(r'detail/clients/$', views.clientListView, name='client_list'),
    re_path(r'api/addstaffmember/$', views.addNewStaffMember.as_view(), name='addnewstaffmember'),
    re_path(r'detail/staff/$', views.staffMemberView, name='staffmemb'),
    re_path(r'detail/hours/$', views.businessHoursView, name='hours'),
    re_path(r'detail/breaks/$', views.businessBreaksView, name='breaks_time'),
    re_path(r'detail/timeoff/$', views.businessTimeOffView, name='timeoff_time'),
    re_path(r'api/update/staff/detail/$', views.UpdateStaffDetails.as_view() , name='updatestaffdetails'),


    re_path(r'creating/$', views.createserviceViews, name='service_create'),
    re_path(r'delete/(?P<pk>\d+)/$', views.deleteserviceViews, name='service_delete'),
    re_path(r'update/(?P<pk>\d+)/$', views.updateserviceViews, name='service_update'),

    re_path(r'deletecategory/(?P<pk>\d+)/$', views.deleteCategoryAPI.as_view(), name='category_delete_view'),

    re_path(r'creatings/$', views.createserviceAPI.as_view(), name='createservice'),
    re_path(r'creatingserv/(?P<pk>\d+)/$', views.createserviceAPII.as_view(), name='createservices'),
    re_path(r'creatingcate/$', views.createcategoryAPI.as_view(), name='createservicecate'),
    re_path(r'deletes/(?P<pk>\d+)/$', views.deleteserviceAPI.as_view(), name='deleteservice'),
    re_path(r'updates/(?P<pk>\d+)/$', views.updateserviceAPI.as_view(), name='updateservice'),

    re_path(r'creatingclient/$', views.createclientAPI.as_view(), name='createclient'),
    re_path(r'deleteclient/(?P<pk>\d+)$', views.deleteclientAPI.as_view(), name='deleteclient'),
    re_path(r'updateclient/(?P<pk>\d+)/$', views.updateclientAPI.as_view(), name='updateclient'),

    re_path(r'reviews/$', views.reviewListView, name='reviewlist'),
    re_path(r'privatetoggle/$', views.changePrivateView.as_view(), name='changePrivate'),

    re_path(r'path/loadsubcategories/$', views.load_subcat, name='ajax_load_subcategories'),
    re_path(r'path/loadservices/$', views.load_services, name='ajax_load_services'),
    re_path(r'ajax/hourmindur/$', views.load_duration, name='ajax_load_duration'),
    re_path(r'ajax/client/$', views.load_client, name='ajax_load_client'),
    re_path(r'ajax/loadevents/$', views.load_events.as_view(), name='ajax_load_events'),
    
    re_path(r'onboarding/check/subdomain/$', views.subdomainCheck.as_view(), name='subdomain'),
    re_path(r'onboarding/$', views.completeViews, name='completeprofile'),
    re_path(r'^updatecompanyform/$',views.updateCompanyDetail.as_view(), name='updateform'),
    re_path(r'^companyformsave/$', views.saveCompanyDetail.as_view(), name='saveDetailForm'),
    re_path(r'^accountFormSave/$', views.personDetailSave.as_view(), name='accountCheck'),
    re_path(r'home/$', views.homepageViews, name='home'),

    re_path(r'getbook/$', views.getBooking.as_view(), name='getBookingId'),

    re_path(r'deletegal/$', views.deleteGalPic.as_view(), name='deletegalpic'),
    re_path(r'galupload/$', views.galImageUpload, name='galleryupload'),
    re_path(r'imageuploads/$', views.headerImageUploads, name='imageuploads'),
    re_path(r'imageupload/$', views.headerImageUpload, name='imageupload'),
    re_path(r'profileimg/$', views.profileImageUpload, name='profileimg'),
    re_path(r'file-upload/$', views.fileUploadView, name='upload'),

    re_path(r'createbusiness/$', views.createNewBusiness, name='newbizcreate'),
    re_path(r'signup/$', views.signupViews, name='bizadminsignup'),
    re_path(r'logout/$', views.LogoutView, name='bizadminlogout'),
    re_path(r'login/$', views.loginViews, name='bizadminlogin'),

    re_path(r'^faq/$', views.faqBusinessViews, name='faqbusiness'),
    re_path(r'addbooking/', views.addBooking.as_view(), name='add_booking'),

    re_path(r'requests/', views.requestListViews, name='requestList'),
    re_path(r'requestedAdd/(?P<pk>\d+)/$', views.addRequestedViews.as_view(), name='addRequested'),
    re_path(r'requestedDelete/(?P<pk>\d+)/$', views.deleteRequestedViews.as_view(), name='deleteRequested'),

    re_path(r'onewaycalendarsync/(?P<pk>\d+)/$', views.calendarScheduleICS.as_view(), name='calendarScheduleICS'),

    re_path(r'^addamenity/$', views.addAmenityAPI.as_view(), name='addamenity'),
    re_path(r'^removeamenity/$', views.removeAmenityAPI.as_view(), name='removeamenity'),
    re_path(r'^addtag/$', views.addTagAPI.as_view(), name='addtag'),
    re_path(r'^removetag/$', views.removeTagAPI.as_view(), name='removetag'),
    re_path(r'^addbusinessh/$',views.saveBusinessHours.as_view(), name='businessHourSave'),

    re_path(r'integration/$', views.integrationsView, name='integrations'),
    re_path(r'integration/zoom/signup', views.integrationZoomSignUp.as_view(), name='zoomsignupintegration'),

    re_path(r'^updatedpass/$', views.updatePassword.as_view(), name='updatepassword'),
    re_path(r'^pricing/$', views.pricingViews, name='pricingBusiness'),
    re_path(r'^$', views.businessadmin, name='bizadminmain'),

]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)