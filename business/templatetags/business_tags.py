from django import template
from ..models import Company
from django.db.models import Avg

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
        if loop <= avg:
            return True
        else:
            return False