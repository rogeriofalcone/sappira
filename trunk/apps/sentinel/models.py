import datetime
from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
	name = models.CharField(max_length=25)

	users = models.ManyToManyField(User, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name',)

	def __unicode__(self):
		return self.name
	
	def get_absolute_url(self):
		return "/team/%i/" % self.id
	
class Patient(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	id_number = models.CharField(max_length=25, blank=True)

	# Basic Audit Trail Data
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	# Responsibility, Permission Data
	team = models.ForeignKey(Team)
	users = models.ManyToManyField(User, blank=True)
	
	# Gender Codes Match Percentile Data
	GENDER_CHOICES = (
		(1, 'Male'),
		(2, 'Female'),
	)
	# Basic Demographic Data
	gender = models.IntegerField(choices=GENDER_CHOICES)
	birth_date = models.DateField()
	location = models.CharField(max_length=25, blank=True)

	presentation = models.TextField(blank=True)
	notes = models.TextField(blank=True)
	
	class Meta:
		ordering = ["last_name"]
		
	def __unicode__(self):
		return self.first_name + ' ' + self.last_name
	
	def get_absolute_url(self):
		return "/patient/%i/" % self.id

	#FIXME no error handling
	def weight(self):
		return self.weight_set.latest().value
		
	def height(self):
		return self.height_set.latest().value
		
	def bmi(self):
	 	return int(self.weight()/((self.height()/100)*(self.height()/100)))
		
	def bmi_class(self):
		bmi = int(self.weight()/((self.height()/100)*(self.height()/100)))
		if bmi < 19:
			return "Underweight"
		elif bmi < 25:
			return "Ideal"
		elif bmi < 30:
			return "Overweight"
		else:
			return "Obese"

class DataPoint(models.Model):
	patient = models.ForeignKey('Patient')
	observed_date = models.DateTimeField(auto_now_add=True)
	notes = models.CharField(max_length=255, blank=True)
	class Meta:
		abstract = True
		ordering = ('observed_date',)
		get_latest_by = ('observed_date',)

	def __unicode__(self):
		#FIXME should say object type or unit too
		return "%s - %s" % (self.patient, self.value)

class Weight(DataPoint):
	value = models.DecimalField(max_digits=5, decimal_places=2)
		
class Height(DataPoint):
	value = models.DecimalField(max_digits=5, decimal_places=2)

class Systolic(DataPoint):
	value = models.IntegerField()

class Diastolic(DataPoint):
	value = models.IntegerField()

class Pulse(DataPoint):
	value = models.IntegerField()
	
class ToDo(models.Model):
	patient = models.ForeignKey('Patient')
	name = models.CharField(max_length=255)
	done = models.BooleanField()
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	#FIXME future features
	#repeating = models.BooleanField(default=False)
	#due_timeuntil = models.IntegerField()
	def __unicode__(self):
		return "%s - %s" % (self.patient, self.name)
	class Meta:
		ordering = ('patient', 'created_date',)
	
class Diet(models.Model):
	DIET_CHOICES = (
		('Clears', 'Clears'),
		('NPO', 'NPO'),
		('Regular', 'Regular'), 
	)
	name = models.CharField(max_length=255)
	patient = models.ForeignKey('Patient')
	
class Prescription(models.Model):
	name = models.CharField(max_length=255)
	patient = models.ForeignKey('Patient')
	
	indication = models.CharField(max_length=255, blank=True)
	dose = models.CharField(max_length=10, blank=True)
	unit = models.CharField(max_length=10, blank=True)
	route = models.CharField(max_length=25, blank=True)
	schedule = models.CharField(max_length=25, blank=True)
	
	active = models.BooleanField(default=True)
	
	start_date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField(auto_now_add=True)
	
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)
	#FIXME ordering is case sensitive
	class Meta:
		ordering = ('name',)

	def __unicode__(self):
		return "%s - %s" % (self.patient, self.name)
	
class Problem(models.Model):
	name = models.CharField(max_length=255)
	patient = models.ForeignKey('Patient')
	prescriptions = models.ManyToManyField(Prescription, blank=True)
	
	active = models.BooleanField(default=True)
	
	start_date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField(auto_now_add=True)
	
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('name', 'patient')
		
	def __unicode__(self):
		return "%s - %s" % (self.patient, self.name)
		
class Medication(models.Model):
	name = models.CharField(max_length=255)
	active_ingredient = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return self.name
		
class Code(models.Model):
	name = models.CharField(max_length=255)
	code = models.CharField(max_length=255)

	def __unicode__(self):
		return self.name

class Percentile(models.Model):
	gender = models.IntegerField()
	age_in_months = models.IntegerField()
	weight_median = models.FloatField()
	weight_variation = models.FloatField()
	weight_cox = models.FloatField()
	height_median = models.FloatField()
	height_variation = models.FloatField()
	height_cox = models.FloatField()