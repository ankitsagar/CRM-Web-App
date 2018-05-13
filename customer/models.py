from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify
from login.models import User
# Create your models here.


class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=120, unique=True)
    phone_no_1 = models.IntegerField()
    phone_no_2 = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=120, null=True, blank=True)
    slug = models.SlugField(editable=False, unique=True)
    added_by = models.ForeignKey(User, null=True)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip_code = models.IntegerField()
    country = models.CharField(max_length=120)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def save(self, **kwargs):
        self.slug = slugify(self.company_name)
        super(CompanyDetails, self).save(**kwargs)

    def __str__(self):
        return self.company_name


STAGES = (
    (1, 'Initial'),  # Lead
    (2, 'Qualification'),  # Opportunity
    (3, 'Closing'),  # Won
    (0, 'Not Qualified'),  # Archive
)


class Contact(models.Model):
    company = models.ForeignKey(CompanyDetails)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    stage = models.IntegerField(choices=STAGES, default=1)
    added_by = models.ForeignKey(User, null=True)
    street = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)
    deal_size = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.company

    def get_address(self):
        return "%s, %s, %s, %s" % (self.street, self.city, self.state, self.zip_code)


class Task(models.Model):
    contact = models.ForeignKey(Contact)
    task = models.CharField(max_length=120)
    due_date = models.DateField()
    task_status = models.BooleanField(default=False)
    task_description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.contact


# def save_customerstatus(sender, instance, *args, **kwargs):
#     customer_status = instance.customerstatus_set.all()
#     if customer_status.count() == 0:
#         status = CustomerStatus()
#         status.company_name = instance
#         status.stage = 'Initial'
#         status.deal_size = 0.00
#         status.save()
#
#
# post_save.connect(save_customerstatus, sender=CustomerInformation)


# class Status(models.Model):
#     contact = models.ForeignKey(Contact)
#
#     def __str__(self):
#         return str(self.contact.phone)