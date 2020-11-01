from django.urls import path ,re_path
from . import views

urlpatterns = [
    re_path(r'^submit/expense/$',views.submit_expence,name='submit_expence'),
    re_path(r'^submit/income/$',views.submit_income,name='submit_income'),
    re_path(r'^accounts/register/$',views.register,name='register'),
]
