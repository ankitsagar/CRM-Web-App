from django.shortcuts import render
from login.decorators import check_role
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from customer.models import CompanyDetails, Contact
# # Create your views here.
#
#
@method_decorator(check_role('Salesman'), name='dispatch')
class Dashboard(ListView):

    template_name = 'salesman/dashboard.html'

    def get_queryset(self):
        return Contact.objects.filter(added_by=self.request.user)
#
#
#
# @method_decorator(check_role('Salesman'), name='dispatch')
# class CustomerDetailView(DetailView):
#     model = CustomerInformation
#     template_name = "salesman/customerinformation_detail.html"
#
#     def get_object(self, queryset=None):
#         obj = super(CustomerDetailView, self).get_object(queryset=queryset)
#
#         if obj.added_by != self.request.user:
#             raise Http404
#         return obj
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(CustomerDetailView, self).get_context_data(*args, **kwargs)
#         context['customer'] = self.get_object()
#         return context
#
#
# @method_decorator(check_role('Salesman'), name='dispatch')
# class CustomerSearchView(View):
#     template_name = "salesman/customer_search.html"
#
#     def get(self, request):
#         first_name = request.GET.get('first_name')
#         last_name = request.GET.get('last_name')
#         phone = request.GET.get('phone')
#         email = request.GET.get('email')
#         company_name = request.GET.get('company_name')
#
#         stage = request.GET.get('stage')
#         follow_up_date_from = request.GET.get('follow_up_date_from')
#         follow_up_date_to = request.GET.get('follow_up_date_to')
#         follow_up_task = request.GET.get('follow_up_task')
#
#         if "search-by-detail" in request.GET:
#
#             if phone:
#                 customer = CustomerInformation.objects.filter(phone=phone)
#
#             elif email:
#                 customer = CustomerInformation.objects.filter(email=email)
#             elif company_name:
#                 customer = CustomerInformation.objects.filter(company_name=company_name)
#             elif first_name and last_name:
#                 customer = CustomerInformation.objects.filter(first_name__icontains=first_name,
#                                                               last_name__icontains=last_name)
#             elif first_name:
#                 customer = CustomerInformation.objects.filter(first_name__icontains=first_name)
#             elif last_name:
#                 customer = CustomerInformation.objects.filter(last_name__icontains=last_name)
#             else:
#                 messages.error(request, "at least one field is required")
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#             context = {
#                 'customer_info': customer
#             }
#             return render(request, "salesman/search_result.html", context)
#
#         if "search-by-status" in request.GET:
#
#             if (follow_up_date_from is not None and follow_up_date_to is None) or (follow_up_date_from is None and follow_up_date_to is not None):
#                 messages.error(request, "both date fields are required")
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#             elif stage and follow_up_date_to and follow_up_date_from and follow_up_task:
#                 customer = CustomerStatus.objects.filter(stage=stage, follow_up_date__range=[follow_up_date_from,
#                                                          follow_up_date_to], follow_up_task=follow_up_task)
#             elif stage and follow_up_date_from and follow_up_date_to:
#                 customer = CustomerStatus.objects.filter(stage=stage, follow_up_date__range=[follow_up_date_from,
#                                                                                              follow_up_date_to])
#
#             # elif follow_up_date_to and follow_up_date_from and follow_up_task:
#             #     customer = CustomerStatus.objects.filter(follow_up_date__range=[follow_up_date_from,
#             #                                              follow_up_date_to], follow_up_task=follow_up_task)
#
#             elif stage and follow_up_task:
#                 customer = CustomerStatus.objects.filter(stage=stage, follow_up_task=follow_up_task)
#
#             # elif follow_up_date_from and follow_up_date_to:
#             #     customer = CustomerStatus.objects.filter(follow_up_date__range=[follow_up_date_from,
#             #                                              follow_up_date_to])
#             # elif follow_up_task:
#             #     customer = CustomerStatus.objects.filter(follow_up_task=follow_up_task)
#
#             elif stage:
#                 customer = CustomerStatus.objects.filter(stage=stage)
#             else:
#                 messages.error(request, "at least one field is required")
#                 return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#             context = {
#                 'customer_status': customer
#             }
#
#             return render(request, "salesman/search_result.html", context)
#
#         return render(request, self.template_name)
#
#
#
#
#
#
#
#
