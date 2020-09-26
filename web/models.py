from django.db import models

from django.contrib.auth.models import User
# Create your models here.
class Expence(models.Model):
    text=models.CharField(max_length=250)
    date=models.DateTimeField()
    amount =models.BigIntegerField()
    user= models.ForeignKey(User,on_delete=models.CASCADE)