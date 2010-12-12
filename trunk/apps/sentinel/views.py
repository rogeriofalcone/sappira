import datetime
import string 
from django.core import serializers
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404, redirect
from django.db.models import Q, F
from django.utils import simplejson
from django.views.generic import list_detail, create_update
from django.forms import ModelForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from models import *

from django import forms
from django.forms import widgets

class PatientForm(ModelForm):
	class Meta:
		model = Patient
		exclude = ('users', 'notes')

class BirthDateForm(forms.Form):
	birth_date = forms.DateField()

class PrescriptionForm(ModelForm):
	class Meta:
		model = Prescription
		
class ProblemForm(ModelForm):
	class Meta:
		model = Problem

class ToDoForm(ModelForm):
	class Meta:
		model = ToDo
		
class DietForm(ModelForm):
	class Meta:
		model = Diet

class DemographicsForm(forms.Form):
	name = forms.CharField()
	gender = forms.CharField(max_length=1, widget=forms.Select(choices=((1,'Male') , (2,'Female'))))
	dob = forms.DateField(label='Birth Date', widget=widgets.TextInput(attrs={'class': '{date:true}'}))
	age = forms.CharField()

#FIXME 
class WeightForm(ModelForm):
	class Meta:
		model = Weight

class HeightForm(ModelForm):
	class Meta:
		model = Height	
		
class VitalsForm(forms.Form):	
	height = forms.IntegerField()
	height_percentile = forms.IntegerField()
	weight = forms.IntegerField()
	weight_percentile = forms.IntegerField()
	bmi = forms.IntegerField(label='Body Mass Index')
	bmi_class = forms.CharField(label='Body Mass Classification')
	pulse = forms.IntegerField()
	systolic = forms.IntegerField()
	diastolic = forms.IntegerField()

class HistoryForm(forms.Form):
	cc = forms.CharField(label='Chief Complaint', max_length=100, widget=widgets.TextInput(attrs={'class': ''}))
	hpi = forms.CharField(widget=widgets.Textarea())
	problems = forms.CharField(widget=widgets.Textarea())
	medications = forms.CharField(widget=widgets.Textarea())
	ros = forms.CharField(widget=widgets.Textarea())
	
# view that displays main template
@login_required		
def index(request):
	patient_form = PatientForm()
	if request.method == 'POST':
		patient_form = PatientForm(request.POST)
		if patient_form.is_valid():
			patient = patient_form.save()
			patient.users.add(request.user)
			return HttpResponseRedirect(reverse(patient_detail, args=[patient.id]))
	return list_detail.object_list(
		request,
		queryset = request.user.patient_set.all(),
		template_object_name = 'patient',
		template_name = 'index.html',
		extra_context = { 
		'patient_form' : patient_form,
		'team_list' : Team.objects.filter(users__id__exact=request.user.id),
		'prescription_list' : Prescription.objects.filter(patient__users__id__contains=request.user.id).order_by('updated_date').reverse()[:10],
		},
	)

def patient_detail(request, object_id):
	problem_form = ProblemForm()
	prescription_form = PrescriptionForm()
	todo_form = ToDoForm()
	patient_form = PatientForm()
	weight_form = WeightForm()
	height_form = HeightForm()
	birth_date_form = BirthDateForm()
	
	if request.method == 'POST':
		if 'problem_form' in request.POST:
			problem_form = ProblemForm(request.POST)
			if problem_form.is_valid():
				problem_form.save()
				return HttpResponseRedirect(reverse(patient_detail, args=[object_id]))	
				
		elif 'prescription_form' in request.POST:
			prescription_form = PrescriptionForm(request.POST)
			if prescription_form.is_valid():
				prescription_form.save()
				return HttpResponseRedirect(reverse(patient_detail, args=[object_id]))	
				
		elif 'todo_form' in request.POST:
			todo_form = ToDoForm(request.POST)
			if todo_form.is_valid():
				todo_form.save()
				return HttpResponseRedirect(reverse(patient_detail, args=[object_id]))	
				
		elif 'patient_form' in request.POST:
			patient_form = PatientForm(request.POST)
			if patient_form.is_valid():
				patient_form.save()
				return HttpResponseRedirect(reverse(patient_detail, args=[object_id]))	
					
		elif 'weight_form' in request.POST:
			weight_form = WeightForm(request.POST)
			if weight_form.is_valid():
				weight_form.save()
				return HttpResponseRedirect(reverse(patient_detail, args=[object_id]))	
				
		elif 'height_form' in request.POST:
			height_form = HeightForm(request.POST)
			if height_form.is_valid():
				height_form.save()
				return HttpResponseRedirect(reverse(patient_detail, args=[object_id]))	
				
		elif 'birth_date_form' in request.POST:
			birth_date_form = BirthDateForm(request.POST)
			print birth_date_form.errors
			if birth_date_form.is_valid():
				patient = Patient.objects.get(pk=object_id)
				patient.birth_date = birth_date_form.cleaned_data['birth_date']
				patient.save()
				return HttpResponseRedirect(reverse(patient_detail, args=[object_id]))	
		
				
	return list_detail.object_detail(
		request,
		queryset = Patient.objects.all(),
		template_object_name = 'patient',
		template_name = 'patient_detail.html',
		object_id = object_id,
		# FIXME filter by user
		extra_context = {
		'prescription_form' : prescription_form,
		'problem_form' : problem_form,
		'problem_form' : problem_form,
		'patient_form' : patient_form,
		'height_form' : height_form,
		'weight_form' : weight_form,
		'team_list' : Team.objects.filter(users__id__exact=request.user.id),
		'patient_list' : request.user.patient_set.all()
		},
	)			
# FIXME need to capute enter submits, errors don't pass through, and should only show up for AJAX requests
def ajax_prescription_add(request):
	if request.is_ajax() and request.method ==	'POST':
		prescription_form = PrescriptionForm(request.POST)
		if prescription_form.is_valid(): 
			prescription_form = prescription_form.save()
	return list_detail.object_detail(
		request,
		queryset = Patient.objects.all(),
		object_id = request.POST['patient'],
		template_object_name = 'patient',
		template_name = 'prescription_list.html',
		extra_context = {
		'prescription_form' : prescription_form,
		},
	)

def ajax_problem_add(request):
	if request.is_ajax() and request.method ==	'POST':
		problem_form = ProblemForm(request.POST)
		if problem_form.is_valid(): 
			problem_form = problem_form.save()
	return list_detail.object_detail(
		request,
		queryset = Patient.objects.all(),
		object_id = request.POST['patient'],
		template_object_name = 'patient',
		template_name = 'problem_list.html',
		extra_context = {
		'problem_form' : problem_form,
		},
	)	

def prescription_stop(request):
	if request.is_ajax() and request.method ==	'POST':
		prescription = Prescription.objects.get(pk=request.POST['prescription'])
		prescription.end_date = datetime.datetime.now()
		prescription.active = False
		prescription.save()
		return list_detail.object_detail(
			request,
			queryset = Patient.objects.all(),
			object_id = prescription.patient.pk,
			template_object_name = 'patient',
			template_name = 'prescription_list.html',
			extra_context = {
			'prescription_form' : PrescriptionForm(),
			},
			)
	else:
		return HttpResponse(status=400)
	
def problem_stop(request):
	if request.is_ajax() and request.method ==	'POST':
		problem = Problem.objects.get(pk=request.POST['problem'])
		problem.end_date = datetime.datetime.now()
		problem.active = False
		problem.save()
		return list_detail.object_detail(
			request,
			queryset = Patient.objects.all(),
			object_id = problem.patient.pk,
			template_object_name = 'patient',
			template_name = 'problem_list.html',
			extra_context = {
			'problem_form' : ProblemForm(),
			},
			)
	else:
		return HttpResponse(status=400)

def todo_stop(request):
	if request.method == 'POST':
		todo = ToDo.objects.get(pk=request.POST['todo'])
		todo.done = True
		todo.save()
	return HttpResponseRedirect(reverse(patient_detail, args=[todo.patient.pk]))	


# view that that returns the JSON result.
def percentile(request):
	gender = request.GET.get('gender', 1)
	age_in_months= int(request.GET.get('age_in_months', 0))
	if ((age_in_months < 0 ) or (age_in_months > 240)):
		age_in_months = 240
	data = Percentile.objects.filter(gender=gender).filter(age_in_months=age_in_months) 
	return HttpResponse(serializers.serialize('json', data), mimetype='application/json')

def ajax_medication(request):
	data = Medication.objects.filter(name__contains=request.GET.get('term', ''))[:10]
	data = [ str(x).title() for x in data ]
	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')
	
def problem(request):	
	data = Problem.objects.filter(name__contains=request.GET.get('term', ''))[:10]
	data = [ x.get_name() for x in data ]
	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')