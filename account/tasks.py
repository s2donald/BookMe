from celery import task
from django.core.mail import send_mail
from django.conf import settings
from .models import Account
from business.models import Company
from consumer.models import Bookings, extraInformation
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twilio.rest import Client

@task
def bizCreatedEmailSent(user_id):
    acct = Account.objects.get(id=user_id)
    company = Company.objects.get(user=acct)
    firstname = acct.first_name
    email = acct.email
    subject = f'Welcome to BookMe Biz!'
    html_message = render_to_string('emailSents/business/created.html', {'acct':acct, 'company':company})
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

@task
def consumerCreatedEmailSent(user_id):
    acct = Account.objects.get(id=user_id)
    email = acct.email
    subject = f'Welcome to BookMe!'
    html_message = render_to_string('emailSents/account/mail_signup.html', {'acct':acct})
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

#This is for the user to remind them of an appointment they have
@task
def reminderEmail(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    if booking.user:
        acct = booking.user
    else:
        acct = booking.guest
    company = booking.company
    service = booking.service
    email = acct.email
    if booking.is_cancelled_user or booking.is_cancelled_company:
        return
        # email = f'noreply@bookme.to'
        # subject = f'Book some '+ company.category.name +' on BookMe!'
        # html_message = render_to_string('emailSents/booking/budge.html', {'acct':acct,'company':company,'service':service, 'booking':booking})
    else:
        subject = f'REMINDER: You have an upcoming appointment with ' + company.business_name + '!'
        html_message = render_to_string('emailSents/booking/reminder.html', {'acct':acct,'company':company,'service':service, 'booking':booking})
    plain_message = strip_tags(html_message)

    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

#This is for the user to confirm the appointment they have
@task
def confirmedEmail(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    if booking.user:
        acct = booking.user
    else:
        acct = booking.guest
    company = booking.company
    service = booking.service
    email = acct.email
    subject = f'Your appointment has been confirmed!'
    html_message = render_to_string('emailSents/booking/bookingSet.html', {'acct':acct,'company':company,'service':service, 'booking':booking})
    plain_message = strip_tags(html_message)

    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent


#This is for the company to confirm the appointment the users have made
@task
def confirmedEmailCompany(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    if booking.user:
        acct = booking.user
    else:
        acct = booking.guest
    company = booking.company
    service = booking.service
    staff = booking.staffmem
    if staff.user:
        email = staff.user.email
    else:
        email = staff.email
    try:
        extra = extraInformation.objects.get(booking=booking)
    except:
        extra = None
    subject = f'You have a new appointment!'
    html_message = render_to_string('emailSents/booking/companyReminder.html', {'staff':staff,'acct':acct,'company':company,'service':service, 'booking':booking, 'extra':extra})
    plain_message = strip_tags(html_message)

    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

@task
def send_sms_confirmed_client(booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
    except Bookings.DoesNotExist:
        return
    if booking.user:
        acct = booking.user
    else:
        acct = booking.guest
    
    phone = acct.phone
    if phone:
        phone = "+1" + str(phone)
    else:
        return
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    staff = booking.staffmem
    if staff.user:
        staff_name = staff.user.first_name
    else:
        staff_name = staff.first_name
    bodymessage = render_to_string('smsSent/consumer/confirmationcons.txt', {'staff_name':staff_name,'booking':booking})
    try:
        message = client.messages.create(
            to=phone, 
            from_=settings.TWILIO_PHONE,
            body=bodymessage)
    except:
        return

@task
def send_sms_reminder_client(booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
    except Bookings.DoesNotExist:
        return
    if booking.is_cancelled_user or booking.is_cancelled_company:
        return

    if booking.user:
        acct = booking.user
    else:
        acct = booking.guest
    
    phone = acct.phone
    if phone:
        phone = "+1" + str(phone)
    else:
        return
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    staff = booking.staffmem
    if staff.user:
        staff_name = staff.user.first_name
    else:
        staff_name = staff.first_name
    bodymessage = render_to_string('smsSent/consumer/remindercons.txt', {'staff_name':staff_name,'booking':booking})
    try:
        message = client.messages.create(
            to=phone, 
            from_=settings.TWILIO_PHONE,
            body=bodymessage)
    except:
        return
        
@task 
def emailRequestServiceClient(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    if booking.user:
        acct = booking.user
    else:
        acct = booking.guest
    company = booking.company
    service = booking.service
    email = acct.email
    subject = f'You have sent an appointment request!'
    html_message = render_to_string('emailSents/booking/bookingRequestSent.html', {'acct':acct,'company':company,'service':service, 'booking':booking})
    plain_message = strip_tags(html_message)

    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

@task
def emailRequestServiceCompany(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    if booking.user:
        acct = booking.user
    else:
        acct = booking.guest
    company = booking.company
    service = booking.service
    staff = booking.staffmem
    if staff.user:
        email = staff.user.email
    else:
        email = staff.email
    try:
        extra = extraInformation.objects.get(booking=booking)
    except:
        extra = None
    subject = f'You have a new appointment request!'
    html_message = render_to_string('emailSents/booking/companyRequestService.html', {'staff':staff,'acct':acct,'company':company,'service':service, 'booking':booking, 'extra':extra})
    plain_message = strip_tags(html_message)

    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

            

@task
def send_sms_requestService_client(booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
    except Bookings.DoesNotExist:
        return
    if booking.user:
        acct = booking.user
    else:
        acct = booking.guest
    
    phone = acct.phone
    if phone:
        phone = "+1" + str(phone)
    else:
        return
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    staff = booking.staffmem
    if staff.user:
        staff_name = staff.user.first_name
    else:
        staff_name = staff.first_name
    bodymessage = render_to_string('smsSent/consumer/requests/bookingrequestSent.txt', {'staff_name':staff_name,'booking':booking})
    try:
        message = client.messages.create(
            to=phone, 
            from_=settings.TWILIO_PHONE,
            body=bodymessage)
    except:
        return


@task
def send_sms_requestService_company(booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
    except Bookings.DoesNotExist:
        return
    if booking.user:
        acct = booking.user
    else:
        acct = booking.guest
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    staff = booking.staffmem
    company = booking.company
    service = booking.service
    staff = booking.staffmem
    if staff.user:
        staff_name = staff.user.first_name
    else:
        staff_name = staff.first_name
    phone = staff.phone
    if phone:
        phone = "+1" + str(phone)
    else:
        return
    bodymessage = render_to_string('smsSent/business/requests/bookingRequestRecieved.txt')
    try:
        message = client.messages.create(
            to=phone, 
            from_=settings.TWILIO_PHONE,
            body=bodymessage)
    except:
        return