from django.db import models
from business.models import Company
# Create your models here.

class formBuilder(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='form')
    label = models.CharField(max_length=50, db_index=True)
    

