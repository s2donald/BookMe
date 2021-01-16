from celery import task
from django.core.mail import send_mail
from .models import Account
from business.models import Company
from consumer.models import Bookings, extraInformation
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
        email = f'noreply@bookme.to'
        subject = f'Book some '+ company.category.name +' on BookMe!'
        html_message = render_to_string('emailSents/booking/budge.html', {'acct':acct,'company':company,'service':service, 'booking':booking})
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