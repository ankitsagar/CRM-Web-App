from django.shortcuts import render
from login.decorators import check_role
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from customer.models import CustomerInformation, CustomerStatus
# Create your views here.


@method_decorator(check_role('Salesman'), name='dispatch')
class Dashboard(ListView):
    model = CustomerInformation
    template_name = 'salesman/customerinformation_list.html'


@method_decorator(check_role('Salesman'), name='dispatch')
class AddCustomer(View):
    template_name = 'salesman/form.html'

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        company_name = request.POST.get('company_name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        country = request.POST.get('country')
        website = request.POST.get('website')

        stage = request.POST.get('stage')
        deal_size = request.POST.get('deal_size')
        follow_up_date = request.POST.get('follow_up_date')
        follow_up_task = request.POST.get('follow_up_task')

        if not first_name or not last_name or not email or not phone or not company_name or not street or not city or not state or not zipcode or not country:
            messages.error(request, "all fields are required")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if CustomerInformation.objects.filter(company_name=company_name).exists():
            messages.error(request, "company already exists")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if CustomerInformation.objects.filter(email=email).exists():
            messages.error(request, "email already exists")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if CustomerInformation.objects.filter(phone=phone).exists():
            messages.error(request, "phone number already exists")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        CustomerInformation.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email,
                                           company_name=company_name, added_by=request.user, street=street, city=city,
                                           state=state, zipcode=zipcode, country=country, website=website)
        company = CustomerInformation.objects.get(company_name=company_name)
        stat = CustomerStatus.objects.get(company_name_id=company.id)

        if deal_size or follow_up_task or follow_up_date:

            if stat.stage == 'Initial' and int(stat.deal_size) == 0 and stat.follow_up_task is None and stat.follow_up_date is None:
                stat.stage = stage
                stat.deal_size = deal_size
                stat.follow_up_date = follow_up_date
                stat.follow_up_task = follow_up_task
                stat.save()

            else:
                CustomerStatus.objects.create(company_name=company, stage=stage, deal_size=deal_size, follow_up_date=
                                              follow_up_date, follow_up_task=follow_up_task)
        messages.success(request, "customer successfully Added")

        return render(request, self.template_name)

    def get(self, request):
        return render(request, self.template_name)


class CustomerDetailView(DetailView):
    model = CustomerInformation




