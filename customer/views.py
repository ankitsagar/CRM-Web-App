from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from .models import *
from django.views.generic.base import TemplateResponseMixin, ContextMixin


def add_company(request):
    if request.user.role == 'Salesman':
        template = 'salesman/add-company.html'
    elif request.user.role == 'Owner':
        template = 'owner/add-company.html'
    else:
        raise Http404

    company_name = request.POST.get('company')
    street = request.POST.get('street')
    postal_code = request.POST.get('postal_code')
    city = request.POST.get('city')
    state = request.POST.get('state')
    country = request.POST.get('country')

    phone_1 = request.POST.get('phone_1')
    phone_2 = request.POST.get('phone_2')
    if not phone_2:
        phone_2 = None

    email = request.POST.get('email')
    website = request.POST.get('website')

    if company_name and street and postal_code and city and state and country and phone_1:
        if not CompanyDetails.objects.filter(
                company_name=company_name).exists():
            CompanyDetails.objects.create(company_name=company_name,
                                          street=street, zip_code=postal_code,
                                          city=city, state=state,
                                          country=country, phone_no_1=phone_1,
                                          phone_no_2=phone_2,
                                          email=email, website=website,
                                          added_by=request.user)
            messages.success(request, 'Company Successfully Added')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Company Already Exist!',
                           extra_tags='danger')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request, template)


class CreateContact(TemplateResponseMixin, ContextMixin, View):

    def get_template_names(self):
        if self.request.user.role == "Salesman":
            return ['salesman/add-contact.html']
        elif self.request.user.role == "Manager":
            return ["manager/add-contact.html"]
        else:
            raise Http404

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        context['companies'] = CompanyDetails.objects.all()

        if request.is_ajax():
            phone = request.GET.get('phone')
            task = request.GET.get('task')
            due_date = request.GET.get('due_date')
            task_description = request.GET.get('task_description')
            task_status = request.GET.get('task_status')
            if task_status == 'true':
                task_status = True
            else:
                task_status = False

            contact = Contact.objects.get(phone=phone)

            if task and due_date:
                Task.objects.create(contact=contact, task=task,
                                    due_date=due_date, task_status=task_status,
                                    task_description=task_description)
                message = 'Task successfully added for customer'

                return JsonResponse({'message': message})
        return render(request, self.get_template_names(), context)

    def post(self, request, **kwargs):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company = request.POST.get('company')
        stage = request.POST.get('stage')
        deal_size = request.POST.get('deal_size')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        if Contact.objects.filter(phone=phone).exists():
            message = 'Customer with this phone no. already exist!'
            return JsonResponse({'message': message})

        elif first_name and last_name and company and phone:
            company = CompanyDetails.objects.get(company_name=company)
            contact = Contact.objects.create(first_name=first_name,
                                             last_name=last_name,
                                             company=company, stage=stage,
                                             phone=phone, street=street,
                                             email=email, city=city,
                                             state=state, added_by=request.user)
            if deal_size:
                contact.deal_size = deal_size

            if postal_code:
                contact.zip_code = postal_code

            contact.save()

            message = 'Contact successfully saved'
            return JsonResponse({'message': message})
        else:
            message = 'Please fill required fields!!'
            return JsonResponse({'message': message})


def add_task(request, **kwargs):
    template = 'salesman/add-task.html'
    contacts = Contact.objects.all().exclude(stage=0)
    context = {
        'contacts': contacts
    }
    if request.is_ajax():
        contact_phone = request.GET.get('contact_phone')

        phone = request.POST.get('phone')
        due_date = request.POST.get('due_date')
        task_description = request.POST.get('task_description')
        task_status = request.POST.get('task_status')
        task = request.POST.get('task')

        if contact_phone:
            contact = Contact.objects.get(phone=contact_phone)
            name = contact.get_full_name()
            company = contact.company.company_name
            address = contact.get_address()
            data = {
                'name': name,
                'company': company,
                'address': address,
            }

            return JsonResponse(data)
        if phone and task and due_date:
            customer = Contact.objects.get(phone=phone)
            task_obj = Task.objects.create(contact=customer, task=task,
                                           due_date=due_date,
                                           task_description=task_description)
            if task_status == 'true':
                task_obj.task_status = True
                task_obj.save()

            return JsonResponse({'message': 'Task successfully created'})

    return render(request, template, context)






























# @method_decorator(login_required, name='dispatch')
# class AddCustomer(View):
#     template_name = 'salesman/form.html'
#
#     def post(self, request):
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         company_name = request.POST.get('company_name')
#         street = request.POST.get('street')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         zipcode = request.POST.get('zipcode')
#         country = request.POST.get('country')
#         website = request.POST.get('website')
#
#         stage = request.POST.get('stage')
#         deal_size = request.POST.get('deal_size')
#         follow_up_date = request.POST.get('follow_up_date')
#         follow_up_task = request.POST.get('follow_up_task')
#
#         if not first_name or not last_name or not email or not phone or not company_name or not street or not city or not state or not zipcode or not country:
#             messages.error(request, "all fields are required")
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#         if CustomerInformation.objects.filter(company_name=company_name).exists():
#             messages.error(request, "company already exists")
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#         if CustomerInformation.objects.filter(email=email).exists():
#             messages.error(request, "email already exists")
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#         if CustomerInformation.objects.filter(phone=phone).exists():
#             messages.error(request, "phone number already exists")
#             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#         CustomerInformation.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email,
#                                            company_name=company_name, added_by=request.user, street=street, city=city,
#                                            state=state, zipcode=zipcode, country=country, website=website)
#         company = CustomerInformation.objects.get(company_name=company_name)
#         stat = CustomerStatus.objects.get(company_name_id=company.id)
#
#         if deal_size or follow_up_task or follow_up_date:
#
#             if stat.stage == 'Initial' and int(stat.deal_size) == 0 and stat.follow_up_task is None and stat.follow_up_date is None:
#                 stat.stage = stage
#                 stat.deal_size = deal_size
#                 stat.follow_up_date = follow_up_date
#                 stat.follow_up_task = follow_up_task
#                 stat.save()
#
#             else:
#                 CustomerStatus.objects.create(company_name=company, stage=stage, deal_size=deal_size, follow_up_date=
#                                               follow_up_date, follow_up_task=follow_up_task)
#         messages.success(request, "customer successfully Added")
#
#         return render(request, self.template_name)
#
#     def get(self, request):
#         return render(request, self.template_name)
