from django.db import models
from cropduster.models import CropDusterField
from django.template.defaultfilters import slugify

from coffin.template import Context, loader

from settings import DART_AD_DEFAULTS


class Position(models.Model):

	name = models.CharField(max_length=255) 

	slug = models.CharField(max_length=255) 

	size = models.CharField(max_length=255)

	class Meta:
		verbose_name_plural = 'Ad Positions'
		
	def __unicode__(self):
		return u'%s' % self.name
		
class Zone(models.Model):

	name = models.CharField(max_length=765) 

	slug = models.CharField(max_length=765)
	
	position = models.ManyToManyField(Position, through='Zone_Position')

	class Meta:
		verbose_name_plural = 'Ad Zones'
		
	def __unicode__(self):
		return u'%s' % self.name		


class Custom_Ad(models.Model):

	url = models.URLField()
	
	image = models.ImageField(upload_to="img/upload/custom_ads", help_text="Image for custom ad")
	
	embed = models.TextField()


	class Meta:
		verbose_name = 'Custom Ad'
		verbose_name_plural = 'Custom Ads'

class Zone_Position(models.Model):

	position = models.ForeignKey(Position)
	
	zone = models.ForeignKey(Zone)
	
	custom_ad = models.ForeignKey(Custom_Ad, blank=True, null=True,)
	
	class Meta:
		verbose_name = 'Enabled Position'
		verbose_name_plural = 'Enabled Positions'

		

class Ad_Page(object):
	""" Base class for Ad and Ad_Factory, keeps track of assigned attributes """

	attributes = DART_AD_DEFAULTS
	_tile = 1

	def __init__(self, site='site', zone='zone', *args, **kwargs):
		self.site = site
		self.zone = zone
		self.attributes.update(kwargs)
			
	def tile(self):
		return self._tile
		self._tile = self._tile + 1

	def get_link(self):
		link = '%s/%s;' % (self.site, self.zone)

		for attr, val in self.attributes.items():

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

		formatted = ''
		index = ''
		for val in values:
			enumerated_attr = attr + str(index)
			formatted += self._format_value(enumerated_attr, val)

			if index == '':
				index = 1
				
			index += 1

		return formatted
	
	
	def get(self, pos, size='0x0', desc_text='', template='ad.html', **kwargs):
		""" main class to get ad tag """
		
		ad = Zone_Position.objects.filter(position__slug=pos, zone__slug=self.zone )
		
		if ad:
		
			if hasattr(ad, "custom_ad"):
				if hasattr(ad.custom_ad, "embed"):
					return ad.custom_ad.embed
				else :
					t = loader.get_template('embed.html')
					c = Context({
						'pos': pos,
						'link': ad.custom_ad.url,
						'image': ad.custom_ad.image,
						'desc_text': desc_text
					})
					return t.render(c)
			else:
				self.attributes.update(kwargs)
				self.attributes['pos'] = pos
				self.attributes['sz'] = size
				
				link = self.get_link()
		
				t = loader.get_template(template)
				c = Context({
					'pos': pos,
					'link': link,
					'tile': self.tile(),
					'desc_text': desc_text
				})
				return t.render(c)
		else :
			return ''
	