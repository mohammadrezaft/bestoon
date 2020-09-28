from django.shortcuts import render
from django.http import JsonResponse
from json import JSONEncoder
from web.models import User ,Token , Expence,Income
from datetime import datetime
  
# Create your views here.
def submit_expence(request):
    """use submits an expence"""
    
    this_token = request.POST ['token']
    this_user=User.objects.filter(token__token= this_token) ()
    if 'date' not in request.POST :
        date=datetime.now()
    
    Expence.objects.create(user=this_user['user'],amunt=request.POST ['amount'],text=request.POST ['text'],date=now)

    requestpost.json()
    return JsonResponse({

        'status':'ok'
    }, encoder=JSONEncoder)