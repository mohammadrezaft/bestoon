from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Passwordresetcodes(models.Model):
    code = models.CharField(max_length=32)
    email = models.CharField(max_length = 120)
    time = models.DateTimeField()
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50) #TODO: do not save password

class Token(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=50)
    def __str__(self):
        return "{}_token".format(self.user)

class Expence(models.Model):
    text=models.CharField(max_length=250)
    date=models.DateTimeField()
    amount =models.BigIntegerField()
    user= models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.user,self.amount)

class Income(models.Model):
    text=models.CharField(max_length=250)
    date=models.DateTimeField()
    amount =models.BigIntegerField()
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return "{}-{}".format(self.date,self.amount)
