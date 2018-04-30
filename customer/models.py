from django.db import models
from django.db.models.signals import post_save

from login.models import User
# Create your models here.


class CompanyDetails(models.Model):
    company_name = models.CharField(max_length=120, unique=True)
    phone_no_1 = models.CharField(max_length=13)
    phone_no_2 = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.CharField(max_length=120, null=True, blank=True)

    added_by = models.ForeignKey(User, null=True)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.company_name


class Contact(models.Model):
    company = models.ForeignKey(CompanyDetails)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=13)
    email = models.EmailField()

    added_by = models.ForeignKey(User, null=True)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=120)
    created = models.DateField(auto_now_add=True, auto_now=False)
    updated = models.DateField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.company

    def get_address(self):
        return "%s, %s, %s, %s" % (self.street, self.city, self.state, self.zip_code)


STAGES = (
    ('Initial', 'Initial'),
    ('Qualification', 'Qualification'),
    ('Closing', 'Closing'),
    ('Not Qualified', 'Not Qualified'),
)


class Status(models.Model):
    contact = models.ForeignKey(Contact)
    stage = models.CharField(max_length=120, choices=STAGES, default='Initial')
    deal_size = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    follow_up_task = models.CharField(max_length=120, blank=True, null=True)
    follow_up_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.contact.phone)


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
