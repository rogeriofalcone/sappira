from django.conf.urls.defaults import *
from django.shortcuts import *
from django.contrib import admin
from models import *
from views import *

admin.autodiscover()
	
urlpatterns = patterns('',
	)
