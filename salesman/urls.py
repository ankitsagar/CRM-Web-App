from django.conf.urls import url

from .views import Dashboard, CustomerDetailView, AddCustomer

urlpatterns = [
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^customer/add/$', AddCustomer.as_view(), name='customer_add'),

]