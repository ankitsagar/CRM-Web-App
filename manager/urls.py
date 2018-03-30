from django.conf.urls import url

from .views import Dashboard

urlpatterns = [
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),

]