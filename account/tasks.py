from celery import task
from django.core.mail import send_mail
from .models import Account

@task
def bizaddedEmailSent(user_id):
    acct = Account.objects.get(id=user_id)
    firstname = acct.first_name
    email = acct.email
    subject = f'Your business page has been added!'
    message = f'Hello '+ firstname +',\n\n'\
        f'Your business page has been created! Now you must add services to your business page, post some pictures on your gallary and start booking in some clients!\n\n'\

    mail_sent = send_mail(subject, 
                            message, 
                            'noreply@gibele.com', 
                            [email], 
                            fail_silently=False)
    return mail_sent