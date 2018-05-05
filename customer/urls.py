from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^add-customer/$', add_company, name='add-customer'),
    # #url(r'^customer/add/$', AddCustomer.as_view(), name='customer_add'),
    # url(r'^customer/search/$', CustomerSearchView.as_view(), name='customer_search'),

]