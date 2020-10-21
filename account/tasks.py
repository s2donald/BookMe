from celery import task
from django.core.mail import send_mail
from .models import Account
from business.models import Company
from consumer.models import Bookings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@task
def bizCreatedEmailSent(user_id):
    acct = Account.objects.get(id=user_id)
    company = Company.objects.get(user=acct)
    firstname = acct.first_name
    email = acct.email
    subject = f'Welcome to Gibele Business!'
    html_message = render_to_string('emailSents/business/created.html', {'acct':acct, 'company':company})
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject, plain_message, 'Gibele <noreply@gibele.com>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

@task
def consumerCreatedEmailSent(user_id):
    acct = Account.objects.get(id=user_id)
    email = acct.email
    subject = f'Welcome to Gibele!'
    html_message = render_to_string('emailSents/account/mail_signup.html', {'acct':acct})
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject, plain_message, 'Gibele <noreply@gibele.com>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

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
    subject = f'REMINDER: You have an upcoming appointment with ' + company.business_name + '!'
    html_message = render_to_string('emailSents/booking/bookingSet.html', {'acct':acct,'company':company,'service':service, 'booking':booking})
    plain_message = strip_tags(html_message)

    mail_sent = send_mail(subject, plain_message, 'Gibele <noreply@gibele.com>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

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

    mail_sent = send_mail(subject, plain_message, 'Gibele <noreply@gibele.com>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

