from django.shortcuts import render
import random
import string
import time
import json
import requests
from django.http import JsonResponse 
from json import JSONEncoder
from web.models import Income,Expence,Token,Passwordresetcodes ,User
from datetime import datetime
import logging
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from postmark import PMMail 
from django.views.decorators.csrf import csrf_exempt
from requests_ntlm import HttpNtlmAuth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 

random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(N))

def crm_name_geter(request):

    url='http://172.16.7.38/DynamicsXRM/api/data/v9.0/contacts?$select=fullname'

    # Issue http request
    response = requests.get(url, auth=HttpNtlmAuth('a.fashtanaghi','!pfV@3861!','hiweb'))

    # Display response content in the console
    response.content
    # Use json module to encode the string content e.g. into a dictionary
    accounts = json.loads(response.content.decode('utf-8'))
    return accounts


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def grecaptcha_verify(request):
    
    data = request.POST
    captcha_rs = data.get('g-recaptcha-response')
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': captcha_rs,
        'remoteip': get_client_ip(request)
    }
    verify_rs = requests.get(url, params=params, verify=True)
    verify_rs = verify_rs.json()
    return verify_rs.get("success", False)



def register(request):
    logger.debug("def register")
    if 'requestcode' in request.POST: #form is filled. if not spam, generate code and save in db, wait for email confirmation, return message
        logger.debug("def register requestcode: " + format(request.POST))
        #is this spam? check reCaptcha
            
        if not grecaptcha_verify(request): # captcha was not correct
            context = {'message': 'کپچای گوگل درست وارد نشده بود. شاید ربات هستید؟ کد یا کلیک یا تشخیص عکس زیر فرم را درست پر کنید. ببخشید که فرم به شکل اولیه برنگشته!'} #TODO: forgot password
            return render(request, 'register.html', context)

        if User.objects.filter(email = request.POST['email']).exists(): # duplicate email
            context = {'message': 'متاسفانه این ایمیل قبلا استفاده شده است. در صورتی که این ایمیل شما است، از صفحه ورود گزینه فراموشی پسورد رو انتخاب کنین. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)

        if not User.objects.filter(username = request.POST['username']).exists(): #if user does not exists
                code = random_str(28)
                now = datetime.now()
                email = request.POST['email']
                password = make_password(request.POST['password'])
                username = request.POST['username'] 
                temporarycode = Passwordresetcodes(
                    email=email, time=now, code=code, username=username, password=password)
                temporarycode.save()
                message = PMMail(api_key = settings.POSTMARK_API_TOKEN,
                                 subject = "فعال سازی اکانت تودو",
                                 sender = "jadi@jadi.net",
                                 to = email,
                                 text_body = "برای فعال سازی ایمیلی تودویر خود روی لینک روبرو کلیک کنید: http://todoer.ir/accounts/register/?email={}&code={}".format(email, code),
                                 tag = "Create account")  
                message.send()
                logger.debug("def register email for http://todoer.ir/accounts/register/?email={}&code={}".format(email, code))
                context = {'message': 'ایمیلی حاوی لینک فعال سازی اکانت به شما فرستاده شده، لطفا پس از چک کردن ایمیل، روی لینک کلیک کنید.'}
                return render(request, 'login.html', context)
        else:
            context = {'message': 'متاسفانه این نام کاربری قبلا استفاده شده است. از نام کاربری دیگری استفاده کنید. ببخشید که فرم ذخیره نشده. درست می شه'} #TODO: forgot password
            #TODO: keep the form data
            return render(request, 'register.html', context)
    elif 'code' in request.GET: # user clicked on code
        logger.debug("def register code: " + format(request.GET))
        email = request.GET['email']
        code = request.GET['code']
        if Passwordresetcodes.objects.filter(code=code).exists(): #if code is in temporary db, read the data and create the user
            new_temp_user = Passwordresetcodes.objects.get(code=code)
            newuser = User.objects.create(username=new_temp_user.username, password=new_temp_user.password, email=email)
            logger.debug("def register user created: {} with code {}".format(newuser.username, code))
            Passwordresetcodes.objects.filter(code=code).delete() #delete the temporary activation code from db
            context = {'message': 'اکانت شما فعال شد. لاگین کنید - البته اگر دوست داشتی'}
            return render(request, 'login.html', context)
        else:
            context = {'message': 'این کد فعال سازی معتبر نیست. در صورت نیاز دوباره تلاش کنید'}
            return render(request, 'login.html', context)
    else:
        context = {'message': ''}
        return render(request, 'register.html', context)
@csrf_exempt
# Create your views here.



def submit_income(request):
    """use submits an income"""
    
    this_token = request.POST.get('token', "1234567")
    this_user=User.objects.filter(token__token= this_token ).get ()
    if 'date' not in request.POST :
        date=datetime.now()
    
    Income.objects.create(user = this_user ,amount= request.POST.get('amount',"5000"),text=request.POST.get('text',"mashin"),date=date)

    return JsonResponse({

        'status':'ok'
    }, encoder=JSONEncoder)




def submit_expence(request):
    """use submits an expence"""
    print('print : ' +request)
    # print(request.POST ['amount'])
    # this_token = request.POST ['amount']
    # this_user=User.objects.filter(token__token= this_token).get ()
    # if 'date' not in request.POST :
    #     date=datetime.now()
    
    # Expence.objects.create(user = this_user ,amount= request.POST['amount'],text=request.POST['text'],date=date)


      

    return JsonResponse({

        'status':'ok'
    }, encoder=JSONEncoder)