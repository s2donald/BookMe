from django.core.mail import get_connection, send_mail, EmailMessage

from celery import task
from django.conf import settings
from .models import Account, WaitListCustomers
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
def sendWaitListEmail(user_id):
    acct = WaitListCustomers.objects.get(id=user_id)
    firstname = acct.first_name
    email = acct.email
    subject = f'Thanks for joining the ShopMe waitlist!'
    html_message = render_to_string('productemail/waitlist_emails.html', {'acct':acct})
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

    email = company.user.email
    new_request = False
    for items in order.items.all():
        if items.product.request:
            new_request = True
    if not new_request:
        subject = f'New Order!'
        message = f'You have recieved a new order. Check it out in the ShopMe dashboard'
    else:
        subject = f'New Order Request!'
        message = f'You have recieved a new order request. Please accept or decline the order within 7 business days.'
    html_message = render_to_string('productemail/vendorConfirm.html', {'company':company, 'message':message})
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

#Completed from dashboard
@task
def order_total_completed(order_id):
    order = Order.objects.get(id=order_id)
    firstname = order.first_name
    email = order.email
    company = order.company
    subject = f'Your ShopMe.to order ' + order.slug + ' has been completed!'
    prod_name = ''
    order_dets =f'Your order, ' + str(order.slug) + ', with ' + company.business_name + ' has been completed.'
    html_message = render_to_string('productadmin/home/emails/orderEmail/baseEmailTemplate.html', {'order':order, 'order_dets':order_dets})
    plain_message = strip_tags(html_message)
    connection = get_connection(
        host=settings.EMAIL1_HOST, 
        port=settings.EMAIL1_PORT, 
        username=settings.EMAIL1_HOST_USER, 
        password=settings.EMAIL1_HOST_PASSWORD, 
        use_tls=settings.EMAIL1_USE_TLS,
        use_ssl=settings.EMAIL1_USE_SSL,
    )
    mail_sent = EmailMessage(subject, html_message,'ShopMe.to <noreply@shopme.to>', [email], connection=connection)
    mail_sent.content_subtype = 'html'
    mail_sent.send()

@task
def order_payment_cancelled(order_id):
    order = Order.objects.get(id=order_id)
    firstname = order.first_name
    email = order.email
    company = order.company
    subject = f'Your ShopMe.to order ' + order.slug + ' has been cancelled'
    order_dets =f'Your order, ' + str(order.slug) + ', with ' + company.business_name + ' has been cancelled. Payments have been refunded.'
    html_message = render_to_string('productadmin/home/emails/orderEmail/baseEmailTemplate.html', {'order':order, 'order_dets':order_dets})
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
    html = render_to_string('productadmin/home/emails/orderEmail/cancelledorderPDF.html',{'order':order,'company':company})
    weasyprint.HTML(string=html).write_pdf(out)
    mail_sent = EmailMessage(subject, html_message,'ShopMe.to <noreply@shopme.to>', [email], connection=connection)
    mail_sent.content_subtype = 'html'
    mail_sent.attach(f'Order ID: {order.slug}.pdf',out.getvalue(),'application/pdf')
    mail_sent.send()

@task
def order_request_accepted(order_id):
    order = Order.objects.get(id=order_id)
    firstname = order.first_name
    email = order.email
    company = order.company
    subject = f'Your ShopMe.to order request ' + order.slug + ' has been accepted!'
    order_dets =f'Your order, ' + str(order.slug) + ', with ' + company.business_name + ' has been accepted.'
    html_message = render_to_string('productadmin/home/emails/orderEmail/baseEmailTemplate.html', {'order':order, 'order_dets':order_dets})
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
    html = render_to_string('productadmin/home/emails/orderEmail/acceptedRequest.html',{'order':order,'company':company})
    weasyprint.HTML(string=html).write_pdf(out)
    mail_sent = EmailMessage(subject, html_message,'ShopMe.to <noreply@shopme.to>', [email], connection=connection)
    mail_sent.content_subtype = 'html'
    mail_sent.attach(f'Order ID: {order.slug}.pdf',out.getvalue(),'application/pdf')
    mail_sent.send()

@task
def order_request_cancelled(order_id):
    order = Order.objects.get(id=order_id)
    firstname = order.first_name
    email = order.email
    company = order.company
    subject = f'Your ShopMe.to order request ' + order.slug + ' was declined'
    order_dets =f'Your order, ' + str(order.slug) + ', with ' + company.business_name + ' has been declined. Payments have been refunded.'
    html_message = render_to_string('productadmin/home/emails/orderEmail/baseEmailTemplate.html', {'order':order, 'order_dets':order_dets})
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
    html = render_to_string('productadmin/home/emails/orderEmail/deniedRequest.html',{'order':order,'company':company})
    weasyprint.HTML(string=html).write_pdf(out)
    mail_sent = EmailMessage(subject, html_message,'ShopMe.to <noreply@shopme.to>', [email], connection=connection)
    mail_sent.content_subtype = 'html'
    mail_sent.attach(f'Order ID: {order.slug}.pdf',out.getvalue(),'application/pdf')
    mail_sent.send()