from django import template
from ..models import Company, Services
from consumer.models import Bookings, Reviews
from django.db.models import Avg
from django.utils import timezone
import pytz
from datetime import timedelta, datetime

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='avg_reviews')
def avg_reviews(loop, ids):
    company = Company.objects.get(pk=ids)
    avg = company.company_reviews.aggregate(Avg('star'))
    avg = avg["star__avg"]
    if avg==None:
        return False
    else:
        if loop - 0.4 <= avg:
            return True
        else:
            return False

##This is used to add a new review for a company
@register.filter(name='inonemonth')
def inonemonth(comp_id, booking_id):
    booking = Bookings.objects.get(pk=booking_id)
    user=booking.user
    company = Company.objects.get(pk=comp_id)
    if user.user_reviews.filter(company=company).exists():
        return False
    if timezone.localtime(booking.start) > timezone.localtime(timezone.now()) - timedelta(days=30):
        return True
    return False

#This is used for when they want to change a review given the customer was serviced within three days
@register.filter(name='changeonemonth')
def changeonemonth(comp_id, review_id):
    review = Reviews.objects.get(pk=review_id)
    if timezone.localtime(review.created) > timezone.localtime(timezone.now()) - timedelta(days=3):
        return True
    return False

@register.filter(name='incancellationperiod')
def incancellationperiod(comp_id, booking_id):
    booking = Bookings.objects.get(pk=booking_id)
    if timezone.localtime(booking.start) - timedelta(hours=booking.company.cancellation) < timezone.localtime(timezone.now()):
        return False
    return True

    