from django.conf.urls import url

from .views import Dashboard, CustomerListView, CustomerDetailView

urlpatterns = [
    url(r'^dashboard/$', CustomerListView.as_view(), name='dashboard'),
    url(r'^(?P<pk>\d+)/$', CustomerDetailView.as_view(), name='customer_detail'),

]