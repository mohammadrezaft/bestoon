from django.urls import path ,re_path
from . import views

urlpatterns = [
    re_path(r'^submit/expense/$',views.submit_expence,name='submit_expence'),
    # path(r'^submit/expence/([-]?[0-9]*)/$', views.submit_expence,name='submit_expence'),
]
