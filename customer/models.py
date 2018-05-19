from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from login.models import User


# Create your models here.


class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=120, unique=True)
    industry_type = models.CharField(max_length=120, null=True, blank=True)
    fax = models.CharField(max_length=120, null=True, blank=True)
    revenue = models.CharField(max_length=120, null=True, blank=True)
    no_of_employee = models.IntegerField(null=True, blank=True)
    phone = models.BigIntegerField(null=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=120, null=True, blank=True)
    slug = models.SlugField(editable=False, unique=True)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=120)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)
    account_owner = models.ForeignKey(User, null=True)

    def save(self, **kwargs):
        self.slug = slugify(self.company_name)
        super(CompanyDetails, self).save(**kwargs)

    def __str__(self):
        return self.company_name


class Contact(models.Model):
    company = models.ForeignKey(CompanyDetails)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.BigIntegerField()
    email = models.EmailField(null=True, blank=True)
    title = models.CharField(max_length=120, null=True, blank=True)

    added_by = models.ForeignKey(User, null=True)
    contact_owner = models.ForeignKey(User, null=True, related_name='owner')
    street = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.company

    def get_address(self):
        return "%s, %s, %s - %s" % (
        self.street, self.city, self.state, self.zip_code)


STATUS = (
    (0, 'Pending'),
    (1, 'Completed'),
    (2, 'Failed')
)
PRIORITIES = (
    (0, 'Low'),
    (1, 'Medium'),
    (2, 'High')
)


class Task(models.Model):
    contact = models.ForeignKey(Contact)
    task = models.CharField(max_length=120)
    due_date = models.DateField()
    priority = models.IntegerField(null=True, choices=PRIORITIES)
    task_owner = models.ForeignKey(User, null=True)
    task_status = models.IntegerField(default=0, choices=STATUS)
    task_description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.task


STAGES = (
    (1, 'Prospecting'),
    (2, 'Opportunity'),
    (3, 'Investigation'),
    (4, 'Presentation'),
    (5, 'Close Won'),
    (0, 'Close Lost'),
)


class Deal(models.Model):
    deal_name = models.CharField(max_length=120)
    company = models.ForeignKey(CompanyDetails)
    amount = models.DecimalField(max_digits=50, decimal_places=2, blank=True,
                                 null=True)
    closing_date = models.DateField()
    stage = models.IntegerField(choices=STAGES, default=1)
    deal_owner = models.ForeignKey(User)
    contact = models.ForeignKey(Contact, null=True)

    def __str__(self):
        return self.company
