from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',

    (r'^$', ('apps.sentinel.views.index')),

	(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
	(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),

	(r'^patient/(\d+)/$', ('apps.sentinel.views.patient_detail')),

	(r'^percentile/$', ('apps.sentinel.views.percentile')),
	(r'^ajax/medication/$', ('apps.sentinel.views.ajax_medication')),

	(r'^ajax/problem/add/$', ('apps.sentinel.views.ajax_problem_add')),
	(r'^problem/stop/$', ('apps.sentinel.views.problem_stop')),
	
	(r'^ajax/prescription/add/$', ('apps.sentinel.views.ajax_prescription_add')),
	(r'^prescription/stop/$', ('apps.sentinel.views.prescription_stop')),

	(r'^todo/stop$', ('apps.sentinel.views.todo_stop')),


    (r'^admin/', include(admin.site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)

# logic for switching between development static serve and production apache settings:
if getattr(settings,'LOCAL_DEV',False):
    # local serving of static files at settings.MEDIA_ROOT
    baseurlregex = r'^static/(?P<path>.*)$'
    urlpatterns = urlpatterns+patterns('',
        (baseurlregex, 'django.views.static.serve',
        {'document_root':  settings.MEDIA_ROOT,'show_indexes': True}),
    )
