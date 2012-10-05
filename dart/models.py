from django.db import models
from cropduster.models import CropDusterField
from django.template.defaultfilters import slugify

from coffin.template import Context, loader

from settings import UPLOAD_PATH


class Position(models.Model):

	name = models.CharField(max_length=255) 

	slug = models.CharField(max_length=255) 

	size = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = 'Ad Positions'
		
	def __unicode__(self):
		return u'%s' % self.name
		
class Zone(models.Model):

	name = models.CharField(max_length=255) 

	slug = models.CharField(max_length=255)
	
	position = models.ManyToManyField(Position, through='Zone_Position')

	class Meta:
		verbose_name_plural = 'Ad Zones'
		
	def __unicode__(self):
		return u'%s' % self.name		


class Custom_Ad(models.Model):

	name = models.CharField(max_length=255, default='')
	
	url = models.URLField()
	
	image = models.ImageField(upload_to=UPLOAD_PATH + "custom_ads", help_text="Image for custom ad")
	
	embed = models.TextField(blank=True, null=True)


	class Meta:
		verbose_name = 'Custom Ad'
		verbose_name_plural = 'Custom Ads'
		
	def __unicode__(self):
		return u"%s" % self.name

class Zone_Position(models.Model):

	position = models.ForeignKey(Position)
	
	zone = models.ForeignKey(Zone)
	
	custom_ad = models.ForeignKey(Custom_Ad, blank=True, null=True,)
	
	def __unicode__(self):
		return u"%s: %s" % (self.zone, self.position)
	
	class Meta:
		verbose_name = 'Enabled Position'
		verbose_name_plural = 'Enabled Positions'

		

class Ad_Page(object):
	""" Base class for Ad and Ad_Factory, keeps track of assigned attributes """
	
	attributes = None
	_tile = 0
	disable_ad_manager = False

	def __init__(self, settings=None, site=None, zone=None, disable_ad_manager=None, *args, **kwargs):
		self.attributes = {}

		# We don't want to set self.attributes 
		settings.pop('attributes', None)

		if settings is not None:
			for setting in settings:
				setattr(self, setting, settings[setting])
			
		if site: self.site = site
		if zone: self.zone = zone
		if disable_ad_manager: self.disable_ad_manager = disable_ad_manager
		self.attributes.update(kwargs)
		
		
			
	def tile(self):
		self._tile = self._tile + 1
		return self._tile
		

	def get_link(self, **kwargs):
		link = '%s/%s;' % (self.site, self.zone)

		for attr, val in self.attributes.items() + kwargs.items():

			# if it is a non-string iteratible object
			if hasattr(val, '__iter__'):
				link += self._format_multiple_values(attr, val)
			else:
				link += self._format_value(attr, val)

		return link

	def _format_value(self, attribute_name, val):

		if attribute_name != 'sz':
			val = slugify(val)

		return "%s=%s;" % (attribute_name, val)

	def _format_multiple_values(self, attr, values):

		formatted = None
		for val in values:
			val = slugify(val)
			if formatted is None:
				formatted = u'{key}={val}'.format(key=attr, val=val)
			else:
				formatted = u'{prev},{key}={val}'.format(prev=formatted, key=attr, val=val) 
		return u'{0};'.format(formatted)
	
	
	def has_ad(self, pos, **kwargs):
		try:
			return Zone_Position.objects.all().filter(position__slug=pos, zone__slug__in=(self.zone,"ros") )[0]
		except:
			return None
			
	def _render_js_ad(self, pos, size, desc_text, template, **kwargs):
		
		
		self.attributes['pos'] = pos
		self.attributes['sz'] = size
		link = self.get_link(**kwargs)
		
		context_vars = {
			'pos': pos,
			'link': link,
			'tile': self.tile(),
			'desc_text': desc_text
		}
		context_vars.update(kwargs)
		
		

		t = loader.get_template(template)
		c = Context(context_vars)
		return t.render(c)

	def _iframe_url(self, pos, size, desc_text, template, **kwargs):
		
		self.attributes['pos'] = pos
		self.attributes['sz'] = size
		link = "/ad/"+self.get_link(**kwargs)

		return link
	
	def get(self, pos, size='0x0', desc_text='', template='dart/ad.html', **kwargs):
		""" main class to get ad tag """

		if self.disable_ad_manager:
			if pos == 'sharing':
				return self._iframe_url(pos, size, desc_text, template, **kwargs)			
			return self._render_js_ad(pos, size, desc_text, template, **kwargs)
		else:
			if 'ad' in kwargs:
				ad = kwargs['ad']
			else :
				ad = self.has_ad(pos, **kwargs)
			
			if ad:
				if ad.custom_ad:
					if ad.custom_ad.embed:
						return ad.custom_ad.embed
					else :
						t = loader.get_template('dart/embed.html')
						c = Context({
							'pos': pos,
							'link': ad.custom_ad.url,
							'image': ad.custom_ad.image,
							'desc_text': desc_text
						})
						return t.render(c)
				else:
					return self._render_js_ad(pos, size, desc_text, template, **kwargs)
			else :
				return ''
