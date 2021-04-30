from django.core.mail import get_connection, send_mail, EmailMessage

from celery import task
from django.conf import settings
from .models import Account
from business.models import Company, CompanyReq
from .models import *
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from twilio.rest import Client
from io import BytesIO
import weasyprint

@task
def bizCreatedEmailSent(user_id):
    acct = Account.objects.get(id=user_id)
    company = Company.objects.get(user=acct)
    firstname = acct.first_name
    email = acct.email
    subject = f'Welcome to ShopMe Biz!'
    html_message = render_to_string('productemail/business_created.html', {'acct':acct, 'company':company})
    plain_message = strip_tags(html_message)
    connection = get_connection(
        host=settings.EMAIL1_HOST, 
        port=settings.EMAIL1_PORT, 
        username=settings.EMAIL1_HOST_USER, 
        password=settings.EMAIL1_HOST_PASSWORD, 
        use_tls=settings.EMAIL1_USE_TLS,
        use_ssl=settings.EMAIL1_USE_SSL,
    )
    mail_sent = send_mail(subject, plain_message,'ShopMe.to <noreply@shopme.to>', [email], html_message=html_message, fail_silently=False, connection=connection)
    return mail_sent


@task
def order_payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    firstname = order.first_name
    email = order.email
    company = order.company
    subject = f'Your ShopMe.to order ' + order.slug + ' has been placed!'
    html_message = render_to_string('productemail/confirmOrder.html', {'order':order, 'company':company})
    plain_message = strip_tags(html_message)
    connection = get_connection(
        host=settings.EMAIL1_HOST, 
        port=settings.EMAIL1_PORT, 
        username=settings.EMAIL1_HOST_USER, 
        password=settings.EMAIL1_HOST_PASSWORD, 
        use_tls=settings.EMAIL1_USE_TLS,
        use_ssl=settings.EMAIL1_USE_SSL,
    )
    out = BytesIO()
    html = render_to_string('productemail/invoice.html',{'order':order,'company':company})
    weasyprint.HTML(string=html).write_pdf(out)
    mail_sent = EmailMessage(subject, html_message,'ShopMe.to <noreply@shopme.to>', [email], connection=connection)
    mail_sent.content_subtype = 'html'
    mail_sent.attach(f'Order ID: {order.slug}.pdf',out.getvalue(),'application/pdf')
    
    mail_sent.send()