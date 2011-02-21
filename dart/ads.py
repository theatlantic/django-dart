from random import randint

from django.template.defaultfilters import slugify

from coffin.template import Context
from coffin.template.loader import get_template

from settings import DART_AD_DEFAULTS

if not DART_AD_DEFAULTS:
	DART_AD_DEFAULTS = {}



class Ad(object):
	""" Base class for Ad and Ad_Factory, keeps track of assigned attributes """

	site = DART_AD_DEFAULTS['site']
	zone = DART_AD_DEFAULTS['zone']

	def __init__(self, pos, size='0x0', **kwargs):
		self.attributes = {}
		self.attributes.update(kwargs)
		self.attributes['pos'] = pos
		self.attributes['sz'] = size

	def get_link(self):
		link = '%s/%s;' % (self.site, self.zone)

		for attr, val in self.attributes.items():

			# if it is a non-string iteratible object
			if hasattr(val, '__iter__'):
				link += self._format_multiple_values(attr, val)
			else:
				link += self._format_value(attr, val)

		return link + '?'

	def _format_value(self, attribute_name, val):
		return "%s=%s;" % (attribute_name, slugify(val))

	def _format_multiple_values(self, attr, values):

		formatted = ''
		index = ''
		for val in values:
			enumerated_attr = attr + str(index)
			formatted += self._format_value(enumerated_attr, val)

			if index == '':
				index = 1
				
			index += 1

		return formatted

	def __unicode__(self):
		""" Prints out the Ad using the ad.html template """

		link = self.get_link()
		t = get_template('ad.html')
		c = Context({'pos': self.attributes['pos'], 'link': link})
		return t.render(c)

class AdFactory(object):

	default_attributes = DART_AD_DEFAULTS

	def __init__(self, **kwargs):
		self.attributes = self.default_attributes.copy()
		self.tile = 0
		self.random = str(randint(1, 10000))
		self.set(**kwargs)

	def set(self, **kwargs):
		self.attributes.update(kwargs)

	def get(self, *args, **kwargs):
		self.tile += 1

		attr = self.attributes.copy()
		attr.update({
			'tile':self.tile,
			'ord': self.random
		})
		attr.update(kwargs)

		return Ad(*args, **attr)