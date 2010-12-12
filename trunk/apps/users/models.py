from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
	('Medical Student', 'Medical Student'),
	('Physician Assistant Student', 'Physician Assistant Student'),
	('Intern', 'Intern'),
	('Resident', 'Resident'),
	('Attending', 'Attending'),
	('Physical Therapist', 'Physical Therapist'),
	('Occupational Therapist', 'Occupational Therapist'),
	('Nurse', 'Nurse'),
	('Social Worker', 'Social Worker'),
)
ROLE_CHOICES = sorted(ROLE_CHOICES, key=lambda x:(x[1], x[0]))

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)

	cell_phone_number = models.CharField(max_length=25, blank=True)
	pager_phone_number = models.CharField(max_length=25, blank=True)
	email = models.CharField(max_length=75, blank=True)
	birth_date = models.DateField()

	def __unicode__(self):
		return self.user.username
	def get_absolute_url(self):
		return "/user/%i/" % self.id