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
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q


@login_required
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


@method_decorator(login_required, name='dispatch')
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


@login_required
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
            street = contact.street
            city = contact.city
            zip_code = contact.zip_code
            state = contact.state
            data = {
                'name': name,
                'company': company,
                'street': street,
                'city': city,
                'zip_code': zip_code,
                'state': state,
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


@method_decorator(login_required, name='dispatch')
class DealAdd(TemplateResponseMixin, ContextMixin, View):
    model = Deal

    def get_template_names(self):
        if self.request.user.role == 'Manager':
            return 'manger/add-deal.html'
        elif self.request.user.role == 'Salesman':
            return 'salesman/add-deal.html'
        else:
            raise Http404

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        context['users'] = User.objects.all().exclude(id=request.user.id)
        context['selected'] = User.objects.get(id=request.user.id)
        context['companies'] = CompanyDetails.objects.all()

        company_name = request.GET.get('company_name')
        if company_name:
            company = CompanyDetails.objects.get(company_name=company_name)
            contact_set = company.contact_set.all()
            contact_list = []

            for contact in contact_set:
                contact_list.append({'id': contact.id,
                                     'name': contact.get_full_name()})
            return JsonResponse({'list': contact_list})

        company = request.GET.get('company')
        if company:
            company = CompanyDetails.objects.get(company_name=company)
            address = company.get_address()
            phone = company.phone
            return JsonResponse({'address': address, 'phone': phone})

        return render(request, self.get_template_names(), context)

    def post(self, request, *args, **kwargs):
        deal_name = request.POST.get('deal_name')
        amount = request.POST.get('amount')
        cl_date = request.POST.get('cl_date')
        stage = request.POST.get('stage')
        owner = request.POST.get('owner')
        company = request.POST.get('company')
        contact = request.POST.get('contact')
        print(company, contact)

        if company and deal_name and cl_date and stage and owner:
            company = CompanyDetails.objects.get(company_name=company)
            owner = User.objects.get(id=owner)
            deal = Deal.objects.create(deal_name=deal_name, stage=stage,
                                       closing_date=cl_date, deal_owner=owner,
                                       company=company)
            if amount:
                deal.amount = amount
            if contact:
                contact = Contact.objects.get(id=contact)
                deal.contact = contact

            deal.save()
            deal_id = deal.id
            messages.success(request, 'Deal Successfully Created')
            return JsonResponse({'message': 'Deal Successfully Created',
                                 'id': deal_id})
        else:
            raise Http404


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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
                        reverse('customer:company',
                                kwargs={'slug': company.slug}))

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


@method_decorator(login_required, name='dispatch')
class DealDetails(DetailView):
    model = Deal

    def get_template_names(self):
        if self.request.user.role == 'Salesman':
            return 'salesman/deal.html'
        elif self.request.user.role == 'Owner':
            return 'owner/deal.html'
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(DealDetails, self).get_context_data(**kwargs)
        context['deal'] = self.get_object()
        if self.get_object().contact:
            context['contacts'] = Contact.objects.filter(
                company__company_name=self.get_object().company).exclude(
                id=self.get_object().contact.id)
        else:
            context['contacts'] = Contact.objects.filter(
                company__company_name=self.get_object().company)
        return context

    def post(self, request, *args, **kwargs):
        deal_id = self.kwargs['pk']
        deal = Deal.objects.get(id=deal_id)
        deal_name = request.POST.get('deal_name')
        amount = request.POST.get('amount')
        cl_date = request.POST.get('cl_date')
        stage = request.POST.get('stage')
        contact = request.POST.get('contact')

        if (request.user.role == 'Manager' or request.user == deal.deal_owner) \
                and (int(deal.stage) != 0 and int(deal.stage) != 5):
            if deal_name and cl_date and stage:
                deal.deal_name = deal_name
                deal.closing_date = cl_date
                deal.stage = stage
                if amount:
                    deal.amount = amount
                else:
                    deal.amount = 0

                if contact:
                    contact = Contact.objects.get(id=contact)
                    deal.contact = contact
                else:
                    deal.contact = None

                deal.save()
                messages.success(request, 'Deal updated')
                return HttpResponseRedirect(
                    self.request.META.get('HTTP_REFERER'))

            else:
                messages.error(request, 'Please fill the required fields!',
                               extra_tags='danger')
                return HttpResponseRedirect(
                    self.request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "You don't have access to edit this deal!",
                           extra_tags='danger')
            return HttpResponseRedirect(
                self.request.META.get('HTTP_REFERER'))


@login_required
def contact_list(request):
    template = "salesman/contact-list.html"
    contacts = Contact.objects.all()
    context = {
        "contacts": contacts
    }
    return render(request, template, context)


@login_required
def company_list(request):
    template = "salesman/company-list.html"
    companies = CompanyDetails.objects.all()
    context = {
        "companies": companies
    }
    return render(request, template, context)


@login_required
def task_list(request):
    template = "salesman/task-list.html"
    tasks = Task.objects.all()
    context = {
        "tasks": tasks
    }
    return render(request, template, context)


@login_required
def deal_list(request):
    template = "salesman/deal-list.html"
    deals = Deal.objects.all().exclude(Q(stage=5) | Q(stage=0))
    context = {
        "deals": deals
    }
    return render(request, template, context)


@login_required
def won_deals(request):
    template = "salesman/won-deals.html"
    deals = Deal.objects.filter(stage=5)
    context = {
        "deals": deals
    }
    return render(request, template, context)


@login_required
def sales_team(request):
    template = "salesman/sales-team.html"
    users = User.objects.all()
    for user in users:
        print(user.date_joined)
    context = {
        "users": users
    }
    return render(request, template, context)
