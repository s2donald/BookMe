import stripe
import json
from django.http import JsonResponse
from djstripe.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import djstripe
from django.http import HttpResponse
from .models import StaffMember, Breaks, StaffWorkingHours
from business.models import Company
from django_hosts.resolvers import reverse

@login_required
def create_sub(request):
    company = get_object_or_404(Company, user=request.user)
    if request.method == 'POST':
        # Reads application/json and returns a response
        data = json.loads(request.body)
        payment_method = data['payment_method']
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)


        try:
            # This creates a new Customer and attaches the PaymentMethod in one API call.
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email=request.user.email,
                invoice_settings={
                    'default_payment_method': payment_method
                }
            )

            stripe.PaymentMethod.attach(
                payment_method,
                customer=customer.id,
            )

            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
            company.stripe_customer = djstripe_customer
            

            # At this point, associate the ID of the Customer object with your
            # own internal representation of a customer, if you have one.
            # print(customer)

            # Subscribe the user to the subscription created
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"],
                    },
                ],
                expand=['latest_invoice.payment_intent'],
            )

            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)

            company.stripe_subscription = djstripe_subscription
            company.save()
            if subscription.status == 'active':
                company.subscriptionplan = 1
                company.save()
            # print(subscription.latest_invoice.payment_intent)
            return JsonResponse(subscription)
        except Exception as e:
            print(e)
            return JsonResponse({'error': (e.args[0])}, status =403)
    else:
        print('error')

        return HTTPresponse('request method not allowed')

def cancelStripeMonthlySubscription(request):
    company = get_object_or_404(Company, user=request.user)
    if request.user.is_authenticated:
        sub_id = company.stripe_subscription.id
        
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        try:
            stripe.Subscription.modify(
                sub_id,
                cancel_at_period_end=True
            )
        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status =403)
    return redirect(reverse('home', host='bizadmin'))