from celery import task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core import mail
from account.models import Account
from business.models import Company, CompanyReq
from consumer.models import Bookings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@task
def addedOnCompanyList(acct_id, company_id):
    acct = Account.objects.get(id=acct_id)
    company = Company.objects.get(id=company_id)
    firstname = acct.first_name
    email = acct.email
    subject = f'Accepted Request!'
    html_message = render_to_string('bizadmin/home/emails/addedOntoClientList.html', {'acct':acct, 'company':company})
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

@task
def requestToBeClient(req_id):
    requested = CompanyReq.objects.get(id=req_id)
    acct = requested.company.user
    client = requested.user
    firstname = acct.first_name
    email = acct.email
    subject = f'New Request: Sign into BookMe to respond'
    html_message = render_to_string('bizadmin/home/emails/requestToCompany.html', {'acct':acct, 'client':client})
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

@task
def appointmentCancelled(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    if booking.user:
        client = booking.user
    else:
        client = booking.guest
    company = booking.company
    service = booking.service
    email = client.email
    subject = f'Appointment Cancelled: Your appointment with ' + company.business_name + ' has been cancelled.'
    html_message = render_to_string('bizadmin/home/emails/cancellationEmail.html', {'client':client, 'booking':booking , 'company':company})
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

@task
def appointmentCancelledCompany(booking_id):
    booking = Bookings.objects.get(id=booking_id)
    if booking.user:
        client = booking.user
    else:
        client = booking.guest

    company = booking.company
    service = booking.service
    email = company.email
    subject = f'Appointment Cancelled: Your appointment with ' + client.first_name + ' has been cancelled.'
    html_message = render_to_string('bizadmin/home/emails/cancelEmailToCompany.html', {'client':client, 'booking':booking , 'company':company})
    plain_message = strip_tags(html_message)
    mail_sent = send_mail(subject, plain_message, 'BookMe.to <noreply@bookme.to>', [email], html_message=html_message, fail_silently=False)
    return mail_sent

@task
def sendMassEmail():
    allcompanies = Company.objects.all()
    emails = []
    subject = f'Merry Christmas and Name Change Announcement from Gibele to BookMe!'
    for comp in allcompanies:
        html_content = render_to_string('emailSents/massEmail/massEmail.html', {'name':comp.user.first_name, 'slug':comp.slug})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, 'BookMe.to <noreply@bookme.to>', [comp.user.email])
        email.attach_alternative(html_content, "text/html")
        emails.append(email)
    mail_sent = mail.get_connection()
    return mail_sent.send_messages(emails)