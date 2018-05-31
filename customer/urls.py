from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^add-company/$', add_company, name='add-company'),
    url(r'^add-contact/$', CreateContact.as_view(), name='add-contact'),
    url(r'^add-task/$', add_task, name='add-task'),
    url(r'^add-deal/$', DealAdd.as_view(), name='add-deal'),
    url(r'^task/(?P<pk>\d+)/$', TaskDetailView.as_view(), name='task'),
    url(r'^contact/(?P<pk>\d+)/$', ContactDetail.as_view(), name='contact'),
    url(r'^deal/(?P<pk>\d+)/$', DealDetails.as_view(), name='deal'),
    url(r'^contact-list/$', contact_list, name='contact-list'),
    url(r'^company-list/$', company_list, name='company-list'),
    url(r'^deal-list/$', deal_list, name='deal-list'),
    url(r'^won-deal/$', won_deals, name='won-deal'),
    url(r'^task-list/$', task_list, name='task-list'),
    url(r'^sales-team/$', sales_team, name='sales-team'),
    url(r'^company/(?P<slug>[\w-]+)/$', Company.as_view(),
        name='company'),
]
