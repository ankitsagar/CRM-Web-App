from django.db import models
from django.db.models.signals import post_save

# Create your models here.

class CustomerInformation(models.Model):
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	title = models.CharField(max_length=120, null=True, blank=True)
	phone = models.CharField(max_length=13)
	email = models.EmailField()
	company_name = models.CharField(max_length=120)
	street = models.CharField(max_length=120)
	city = models.CharField(max_length=120)
	state = models.CharField(max_length=120)
	zipcode = models.CharField(max_length=120)
	country = models.CharField(max_length=120)
	website = models.CharField(max_length=120, null=True, blank=True)
	created = models.DateField(auto_now_add=True, auto_now=False)
	updated = models.DateField(auto_now_add=False, auto_now=True)
	

	def __str__(self):
		return self.company_name

	def get_full_name(self):
		return "%s %s" % (self.first_name, self.last_name)

	def get_address(self):
		return "%s, %s, %s, %s" %(self.street, self.city, self.state, self.zipcode)


STAGES = (
	('initial', 'Initial'),
	('qualification', 'Qualification'),
	('presentation', 'Presentation'),
	('evaluation', 'Evaluation'),
	('closing', 'Closing')
)

class CustomerStatus(models.Model):
	company_name = models.ForeignKey(CustomerInformation)
	stage = models.CharField(max_length=120, choices=STAGES, default='Initial')
	deal_size = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
	follow_up_task = models.CharField(max_length=120, blank=True, null=True)
	follow_up_date = models.DateField(null=True, blank=True)

	def __str__(self):
		return str(self.company_name.id)

def save_customerstatus(sender, instance, *args, **kwargs):
	customer_status = instance.customerstatus_set.all()
	if customer_status.count() == 0:
		status = CustomerStatus()
		status.company_name = instance
		status.stage = 'Initial'
		status.deal_size = 0.00
		status.save()

post_save.connect(save_customerstatus, sender=CustomerInformation)
		




