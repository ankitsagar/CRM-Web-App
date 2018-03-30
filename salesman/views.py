from django.shortcuts import render
from login.decorators import check_role
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from customer.models import CustomerInformation
# Create your views here.


@method_decorator(check_role('Salesman'), name='dispatch')
class Dashboard(View):
    template_name = 'salesman/dashboard.html'

    def get(self, request, *args, **kwargs):
        template = self.template_name
        return render(request, template)

@method_decorator(check_role('Salesman'), name='dispatch')
class CustomerListView(ListView):
    model = CustomerInformation
    template_name = 'salesman/customerinformation_list.html'


class CustomerDetailView(DetailView):
    model = CustomerInformation
