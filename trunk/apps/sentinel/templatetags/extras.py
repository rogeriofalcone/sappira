import re
import sys
from django.template import Node, NodeList, Template, Context, Variable, Library
from django.template import get_library, Library, InvalidTemplateLibrary
from django.template import TemplateSyntaxError, VariableDoesNotExist, BLOCK_TAG_START, BLOCK_TAG_END, VARIABLE_TAG_START, VARIABLE_TAG_END, SINGLE_BRACE_START, SINGLE_BRACE_END, COMMENT_TAG_START, COMMENT_TAG_END
from django.template.smartif import IfParser, Literal
from django.utils.translation import ugettext, ungettext
from django.utils.safestring import mark_safe, SafeData
from django.conf import settings
from django.utils import formats
from django.utils.encoding import force_unicode, iri_to_uri
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe, SafeData
from django.utils.translation import ugettext, ungettext
import datetime
import time

from django.utils.tzinfo import LocalTimezone

register = Library()
	
def timesince(d, now=None):
	"""
	Takes two datetime objects and returns the time between d and now
	as a nicely formatted string, e.g. "10 minutes".  If d occurs after now,
	then "0 minutes" is returned.

	Units used are years, months, weeks, days, hours, and minutes.
	Seconds and microseconds are ignored.  Up to two adjacent units will be
	displayed.	For example, "2 weeks, 3 days" and "1 year, 3 months" are
	possible outputs, but "2 weeks, 3 hours" and "1 year, 5 days" are not.

	Adapted from http://blog.natbat.co.uk/archive/2003/Jun/14/time_since
	"""
	chunks = (
		(60 * 60 * 24 * 365, lambda n: ungettext('year', 'years', n)),
		(60 * 60 * 24 * 30, lambda n: ungettext('month', 'months', n)),
		(60 * 60 * 24 * 7, lambda n : ungettext('week', 'weeks', n)),
		(60 * 60 * 24, lambda n : ungettext('day', 'days', n)),
		(60 * 60, lambda n: ungettext('hour', 'hours', n))
	)
	# Convert datetime.date to datetime.datetime for comparison.
	if not isinstance(d, datetime.datetime):
		d = datetime.datetime(d.year, d.month, d.day)
	if now and not isinstance(now, datetime.datetime):
		now = datetime.datetime(now.year, now.month, now.day)
	if not now:
		if d.tzinfo:
			now = datetime.datetime.now(LocalTimezone(d))
		else:
			now = datetime.datetime.now()

	# ignore microsecond part of 'd' since we removed it from 'now'
	delta = now - (d - datetime.timedelta(0, 0, d.microsecond))
	since = delta.days * 24 * 60 * 60 + delta.seconds
	if since <= 0:
		# d is in the future compared to now, stop processing.
		return u'0 ' + ugettext('minutes')
	for i, (seconds, name) in enumerate(chunks):
		count = since // seconds
		if count != 0:
			break
	s = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}
	if i + 1 < len(chunks):
		# Now get the second item
		seconds2, name2 = chunks[i + 1]
		count2 = (since - (seconds * count)) // seconds2
		if count2 != 0:
			s += ugettext(', %(number)d %(type)s') % {'number': count2, 'type': name2(count2)}
	return s

def timesinceshort(value, arg=None):
	"""Formats a date as the time since that date (i.e. "4 days, 6 hours")."""
	if not value:
		return u''
	try:
		if arg:
			return timesince(value, arg)
		return timesince(value)
	except (ValueError, TypeError):
		return u''
timesinceshort.is_safe = False

register.filter(timesinceshort)