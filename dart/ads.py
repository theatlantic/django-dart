from random import randint

from django.template.loader import get_template
from django.template import Context
from django.template.defaultfilters import slugify

from settings import DART_AD_DEFAULTS

if not DART_AD_DEFAULTS:
	DART_AD_DEFAULTS = {}

class Ad(object):
	""" Base class for Ad and Ad_Factory, keeps track of assigned attributes """

	try:
		shared_attributes = DART_AD_DEFAULTS['attributes']
	except KeyError:
		shared_attributes = {}

	site = DART_AD_DEFAULTS['site']
	zone = DART_AD_DEFAULTS['zone']

	def __init__(self, pos, size='0x0', **kwargs):

		self.attributes = self.shared_attributes.copy()
		self.attributes.update(kwargs)
		self.attributes['ord'] = str(randint(1, 5000))
		self.attributes['pos'] = pos
		self.attributes['sz'] = size

	def get_link(self):
		link = self.site + '/' + self.zone

		for attr, val in self.attributes.items():

			# if it is a non-string iteratible object
			if hasattr(val, '__iter__'):
				# join together with commas
				val = ",".join( map(slugify,val) )
			else:
				val = slugify(val)

			link = link + ';' + attr + '=' + val

		return link + '?'

	def __unicode__(self):
		""" Prints out the Ad using the ad.html template """
		link = self.get_link()
		t = get_template('ad.html')
		c = Context({'pos': self.attributes['pos'], 'link': link})
		return t.render(c)

	@staticmethod
	def set(**kwargs):
		Ad.shared_attributes.update(kwargs)