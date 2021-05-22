from django.conf.urls import url, include
from django.contrib import admin
from django.urls import re_path, path
from django.contrib.auth import views as auth_views
from . import views
from businessadmin import stripe_views
app_name = 'productadmin'
urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('adminpagefordjangosuuwoop/', admin.site.urls),
    path('adminpagefordjangosuuwoop/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),

    re_path(r'businesspage/photo/$', views.businessPhotoView, name='photos'),#Changed
    re_path(r'businesspage/amentities/$', views.businessAmenitiesView, name='amenities'),#changed
    re_path(r'businesspage/customization/$', views.businessPageCustomization, name='bpagecustomization'),#changed
    re_path(r'api/addcustomize/theme/$', views.customThemeAPI.as_view(), name='toggletheme'),

    re_path(r'dashboard/orders/$', views.orderView, name='orders'),
    re_path(r'dashboard/shipping/$', views.shippingView, name='shipping'),
    re_path(r'dashboard/shipping/add_shipping/$', views.addshippingView, name='addshipping'),
    re_path(r'api/dashboard/shipping/get_country_list/$', views.getCountriesListAPI.as_view(), name='getCountriesList'),
    re_path(r'api/dashboard/shipping/create_shipping/$', views.createshippingZoneViewAPI.as_view(), name='createshippingzone'),
    re_path(r'api/grabthemodalorder/$', views.modalGetOrderType.as_view(), name='ordermodalview'),

    re_path(r'dashboard/profile/security/$',views.profileSecurityViews, name='security'),#Changed
    re_path(r'dashboard/profile/notifs/$', views.notifViews, name='notifications'),
    re_path(r'dashboard/profile/payments/$', views.paymentsView.as_view(), name='staff_payments'),
    re_path(r'dashboard/profile/payments/recurring/$', views.payMonthlyView, name='payments_to_bookme'),
    re_path(r'dashboard/profile/payments/recurring/stripe-webhook/$', views.webhook_received.as_view(), name='webhook_received_stripe'),
    re_path(r'dashboard/profile/payments/authorize/$', views.StripeAuthorizeView.as_view(), name='stripe_authorize'),
    re_path(r'dashboard/profile/payments/deauthorize/$', views.StripeDeauthorizeView.as_view(), name='stripe_deauthorize'),
    re_path(r'dashboard/profile/payments/oauth/callback', views.StripeAuthorizeCallbackView.as_view(), name='authorize_callback'),
    re_path(r'dashboard/profile/$',views.profileViews, name='profile'),

    re_path(r'update/emailinfo/$', views.updateEmailSetting.as_view(), name='emailUpdate'),
    re_path(r'update/notes/$', views.notesUpdate.as_view(), name='notesUpdate'),

    re_path('darkmode/', views.changeDarkMode.as_view(), name='changeDarkMode'),

    re_path(r'detail/info/$', views.compinfoViews, name='information'),#Changed
    re_path(r'detail/products/$', views.servicesDetailView, name='service_detail'),
    
    re_path(r'detail/clients/$', views.clientListView, name='client_list'),
    re_path(r'detail/staff/$', views.staffMemberView, name='staffmemb'),
    re_path(r'detail/hours/$', views.businessHoursView, name='hours'),
    re_path(r'detail/breaks/$', views.businessBreaksView, name='breaks_time'),
    re_path(r'detail/timeoff/$', views.businessTimeOffView, name='timeoff_time'),
    re_path(r'creating/$', views.createproductViews, name='product_create'),#Created Product

    re_path(r'deletecategory/(?P<pk>\d+)/$', views.deleteCategoryAPI.as_view(), name='category_delete_view'),

    re_path(r'creatingproduct/(?P<pk>\d+)/$', views.createserviceAPII.as_view(), name='createproducts'),#needed
    re_path(r'deletes/(?P<pk>\d+)/$', views.deleteserviceAPI.as_view(), name='deleteproduct'),#Updated
    re_path(r'updates/(?P<pk>\d+)/$', views.updateserviceAPI.as_view(), name='updateproduct'),#Updated
    re_path(r'adddropdown/(?P<pk>\d+)/$', views.addDropdownOption.as_view(), name='adddropdownprod'),#Added
    re_path(r'addquestion/(?P<pk>\d+)/$', views.addQuestionOption.as_view(), name='addquestionprod'),#Added 
    re_path(r'addgallaryproductpic/(?P<pk>\d+)/$', views.addProductGallaryPic.as_view(), name='addproductgallaryphotos'),
    re_path(r'removedropdown/(?P<pk>\d+)/$', views.removeDropDownOption.as_view(), name='removedropdown'),#added
    re_path(r'removequestion/(?P<pk>\d+)/$', views.removeQuestionOption.as_view(), name='removequestion'),#added
    re_path(r'onboarding/check/subdomain/$', views.subdomainCheck.as_view(), name='subdomain'),
    
    re_path(r'creatingclient/$', views.createclientAPI.as_view(), name='createclient'),
    re_path(r'deleteclient/(?P<pk>\d+)$', views.deleteclientAPI.as_view(), name='deleteclient'),

    re_path(r'reviews/$', views.reviewListView, name='reviewlist'),
    re_path(r'privatetoggle/$', views.changePrivateView.as_view(), name='changePrivate'),

    re_path(r'path/loadsubcategories/$', views.load_subcat, name='ajax_load_subcategories'),
    re_path(r'path/loadservices/$', views.load_services, name='ajax_load_services'),
    
    re_path(r'onboarding/$', views.completeViews, name='completeprofile'),
    re_path(r'^companyformsave/$', views.saveCompanyDetail.as_view(), name='saveDetailForm'),
    re_path(r'^accountFormSave/$', views.personDetailSave.as_view(), name='accountCheck'),
    re_path(r'home/$', views.homepageViews, name='home'),#Changed

    re_path(r'getbook/$', views.getBooking.as_view(), name='getBookingId'),

    re_path(r'deletegal/$', views.deleteGalPic.as_view(), name='deletegalpic'),
    re_path(r'galupload/$', views.galImageUpload, name='galleryupload'),
    re_path(r'imageuploads/$', views.headerImageUploads, name='imageuploads'),
    re_path(r'profileimg/$', views.profileImageUpload, name='profileimg'),
    re_path(r'file-upload/$', views.fileUploadView, name='upload'),

    re_path(r'createbusiness/$', views.createNewBusiness, name='newbizcreate'),
    re_path(r'signup/$', views.signupViews, name='bizadminsignup'),
    re_path(r'logout/$', views.LogoutView, name='bizadminlogout'),
    re_path(r'login/$', views.loginViews, name='bizadminlogin'),

    re_path(r'^faq/$', views.faqBusinessViews, name='faqbusiness'),

    re_path(r'^addamenity/$', views.addAmenityAPI.as_view(), name='addamenity'),
    re_path(r'^removeamenity/$', views.removeAmenityAPI.as_view(), name='removeamenity'),
    re_path(r'^addtag/$', views.addTagAPI.as_view(), name='addtag'),
    re_path(r'^removetag/$', views.removeTagAPI.as_view(), name='removetag'),
    re_path(r'integration/zoom/signup', views.integrationZoomSignUp.as_view(), name='zoomsignupintegration'),
    #Stripe Integration
    path("create-sub", stripe_views.create_sub, name="create_sub"), #add
    path("complete", views.completeSubscriptionPayment, name="complete_subscription_stripe"),
    path("cancel", stripe_views.cancelStripeMonthlySubscription, name="cancel_subscription_stripe"),

    re_path(r'^updatedpass/$', views.updatePassword.as_view(), name='updatepassword'),
    re_path(r'^pricing/$', views.pricingViews, name='pricingBusiness'),
    re_path(r'^$', views.businessadmin, name='bizadminmain'),

]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)