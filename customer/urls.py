from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^add-company/$', add_company, name='add-company'),
    url(r'^add-contact/$', CreateContact.as_view(), name='add-contact'),
    url(r'^add-task/$', add_task, name='add-task'),
    url(r'^task/(?P<pk>\d+)/$', TaskDetailView.as_view(), name='task'),
    url(r'^contact/(?P<pk>\d+)/$', ContactDetail.as_view(), name='contact'),
    url(r'^company/(?P<slug>[\w-]+)/$', Company.as_view(),
        name='company'),
    url(r'^update-contact/(?P<pk>\d+)/$', update_contact_detail,
        name='update-contact'),

    # url(r'^customer/search/$', CustomerSearchView.as_view(), name='customer_search'),

]
