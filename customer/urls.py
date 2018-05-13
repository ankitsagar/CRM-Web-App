from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^add-company/$', add_company, name='add-company'),
    url(r'^add-contact/$', CreateContact.as_view(), name='add-contact'),
    # url(r'^customer/search/$', CustomerSearchView.as_view(), name='customer_search'),

]