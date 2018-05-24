from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
import datetime
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
    industry = request.POST.get('industry')
    revenue = request.POST.get('revenue')
    employees = request.POST.get('employees')
    street = request.POST.get('street')
    postal_code = request.POST.get('postal_code')
    city = request.POST.get('city')
    state = request.POST.get('state')
    country = request.POST.get('country')

    phone = request.POST.get('phone')
    fax = request.POST.get('fax')

    email = request.POST.get('email')
    website = request.POST.get('website')

    if company_name and street and postal_code and city and state and country and phone:
        if not CompanyDetails.objects.filter(
                company_name=company_name).exists():
            company = CompanyDetails.objects.create(company_name=company_name,
                                                    street=street,
                                                    zip_code=postal_code,
                                                    city=city, state=state,
                                                    country=country,
                                                    phone=phone, fax=fax,
                                                    industry_type=industry,
                                                    email=email,
                                                    website=website,
                                                    account_owner=request.user)

            if revenue:
                company.revenue = revenue

            if employees:
                company.no_of_employee = employees

            company.save()

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
            return 'salesman/add-contact.html'
        elif self.request.user.role == "Manager":
            return "manager/add-contact.html"
        else:
            raise Http404

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        context['selected'] = request.user
        context['users'] = User.objects.all().exclude(id=request.user.id)
        context['companies'] = CompanyDetails.objects.all()

        if request.is_ajax():
            phone = request.GET.get('phone')
            task = request.GET.get('task')
            due_date = request.GET.get('due_date')
            task_description = request.GET.get('task_description')
            task_status = request.GET.get('task_status')
            priority = request.GET.get('priority')

            if not task_status:
                task_status = 0

            contact = Contact.objects.get(phone=phone)

            if task and due_date:
                Task.objects.create(contact=contact, due_date=due_date,
                                    priority=priority, task_status=task_status,
                                    task_owner=request.user, task=task,
                                    task_description=task_description)
                message = 'Task successfully added for customer'

                contact_id = contact.id
                return JsonResponse({'message': message, 'id': contact_id})
        return render(request, self.get_template_names(), context)

    def post(self, request, **kwargs):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company = request.POST.get('company')
        title = request.POST.get('title')
        owner = request.POST.get('owner')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        if owner:
            owner = User.objects.get(id=owner)

        if Contact.objects.filter(phone=phone).exists():
            message = 'Customer with this phone no. already exist!'
            return JsonResponse({'message': message})

        elif first_name and last_name and company and phone:
            company = CompanyDetails.objects.get(company_name=company)
            contact = Contact.objects.create(first_name=first_name,
                                             last_name=last_name,
                                             contact_owner=owner,
                                             company=company, title=title,
                                             phone=phone, street=street,
                                             email=email, city=city,
                                             state=state, added_by=request.user)

            if postal_code:
                contact.zip_code = postal_code

            contact.save()
            contact_id = contact.id

            message = 'Contact successfully saved'
            return JsonResponse({'message': message, 'id': contact_id})
        else:
            message = 'Please fill required fields!!'
            return JsonResponse({'message': message})


def add_task(request, **kwargs):
    template = 'salesman/add-task.html'
    contacts = Contact.objects.all()
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
        priority = request.POST.get('priority')

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
                                           due_date=due_date, priority=priority,
                                           task_owner=request.user,
                                           task_description=task_description)
            if task_status:
                task_obj.task_status = task_status
                task_obj.save()

            messages = 'Task successfully created'
            task_id = task_obj.id

            return JsonResponse({'message': messages, 'id': task_id})

    contact_id = request.GET.get('contact_id')
    if contact_id:
        contact_info = Contact.objects.get(id=contact_id)
        context['contact_info'] = contact_info

    return render(request, template, context)


class TaskDetailView(DetailView):
    model = Task

    def get_template_names(self):
        if self.request.user.role == 'Salesman':
            template_name = "salesman/task.html"
        elif self.request.user.role == 'Manager':
            template_name = "manager/task.html"

        return template_name

    def get_object(self, queryset=None):
        obj = super(TaskDetailView, self).get_object(queryset=queryset)

        # if obj.contact.added_by != self.request.user:
        #     raise Http404
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(TaskDetailView, self).get_context_data(*args, **kwargs)
        context['task'] = self.get_object()
        return context

    def post(self, *args, **kwargs):
        task_id = self.kwargs['pk']
        task = Task.objects.get(id=task_id)

        if task.task_status == 0 and (self.request.user.role == "Manager" or
                                      self.request.user == task.task_owner):
            status = self.request.POST.get('task_status')
            subject = self.request.POST.get('task')
            due_date = self.request.POST.get('due_date')
            task_desc = self.request.POST.get('task_desc')
            priority = self.request.POST.get('priority')

            task.priority = priority
            task.task = subject
            task.task_description = task_desc
            task.task_status = status
            print(priority, status)
            if subject and due_date:
                task.due_date = due_date
                task.save()
                messages.success(self.request, "Task successfully updated",
                                 extra_tags='success')
            else:
                messages.error(self.request, "Please fill the required fields",
                               extra_tags='danger')
        else:
            messages.error(self.request,
                           "You don't have access to edit this task",
                           extra_tags='danger')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class ContactDetail(DetailView):
    model = Contact

    def get_template_names(self):
        if self.request.user.role == 'Salesman':
            template = 'salesman/contact.html'

        elif self.request.user.role == 'Owner':
            template = 'owner/contact.html'

        else:
            raise Http404

        return template

    def get_object(self, queryset=None):
        obj = super(ContactDetail, self).get_object(queryset=None)
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(ContactDetail, self).get_context_data(*args, **kwargs)
        context['contact'] = self.get_object()
        context['users'] = User.objects.all().exclude(
            id=self.get_object().contact_owner.id)
        return context

    def post(self, request, *args, **kwargs):
        contact_id = kwargs['pk']
        contact = Contact.objects.get(id=contact_id)

        phone = request.POST.get('phone')
        if phone:
            contact.phone = phone
        else:
            raise Http404

        zip_code = request.POST.get('postal_code')
        if zip_code:
            contact.zip_code = zip_code
        else:
            contact.zip_code = None

        contact.email = request.POST.get('email')
        contact.street = request.POST.get('street')
        contact.city = request.POST.get('city')
        contact.state = request.POST.get('state')
        if request.user == contact.contact_owner or request.user.role == 'Manager':
            messages.success(request, "Contact successfully updated",
                             extra_tags='success')
            contact.save()
        else:
            messages.error(request, "You Don't have access to this contact!",
                           extra_tags='danger')

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class Company(DetailView):
    model = CompanyDetails

    def get_template_names(self):
        if self.request.user.role == 'Salesman':
            template = 'salesman/company.html'
        elif self.request.user.role == 'Owner':
            template = 'owner/company.html'
        else:
            raise Http404
        return template

    def get_context_data(self, **kwargs):
        context = super(Company, self).get_context_data(**kwargs)
        context['company'] = self.get_object()
        context['contact_set'] = self.get_object().contact_set.all()
        context['users'] = User.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        company_id = request.POST.get("company_id")

        if company_id:
            company = CompanyDetails.objects.get(id=company_id)
            company_name = request.POST.get("company")
            industry = request.POST.get("industry")
            revenue = request.POST.get("revenue")
            phone = request.POST.get("phone")
            fax = request.POST.get("fax")
            email = request.POST.get("email")
            website = request.POST.get("website")
            employees = request.POST.get("employees")
            owner = request.POST.get("owner")
            street = request.POST.get("street")
            city = request.POST.get("city")
            zip_code = request.POST.get("postal_code")
            state = request.POST.get("state")
            country = request.POST.get("country")

            if request.user.role == "Manager" \
                    or request.user == company.account_owner:

                if company_name and phone and zip_code and state and city \
                        and street and state and country and owner:
                    company.company_name = company_name
                    company.industry_type = industry

                    if revenue:
                        company.revenue = revenue
                    else:
                        company.revenue = None

                    company.fax = fax
                    company.email = email
                    company.website = website
                    company.state = state
                    company.street = street
                    company.city = city
                    company.zip_code = zip_code
                    company.country = country

                    if employees:
                        company.no_of_employee = employees
                    else:
                        company.no_of_employee = None

                    owner = User.objects.get(id=owner)
                    company.account_owner = owner
                    company.save()
                    messages.success(request, "Details successfully updated",
                                     extra_tags='success')

                    return HttpResponseRedirect(
                        reverse('customer:company', kwargs={'slug': company.slug}))

                else:
                    messages.error(request, "Please fill the required fields",
                                   extra_tags='danger')

                    return HttpResponseRedirect(
                        self.request.META.get('HTTP_REFERER'))

            else:
                messages.error(request,
                               "You don't have access to edit these details",
                               extra_tags='danger')

                return HttpResponseRedirect(
                    self.request.META.get('HTTP_REFERER'))




















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
