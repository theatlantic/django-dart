from django.db import models
from cropduster.models import CropDusterField
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from coffin.template import Context, loader

from settings import UPLOAD_PATH

STANDARD_AD_SIZES = (
	(0, "Any Size | 0x0"),
	(1, "Custom Size"),
	(2, "Large Rectangle | 336x280"),
	(3, "Medium Rectangle | 300x250"),
	(4, "Square Pop-up | 250x250"),
	(5, "Vertical Rectangle | 240x400"),
	(6, "Rectangle | 180x150"),
	(7, "Leaderboard | 728x90"),
	(8, "Full Banner | 468x60"),
	(9, "Half Banner | 234x60"),
	(10, "Button 1 | 120x90"),
	(11, "Button 2 | 120x60"),
	(12, "Micro Bar | 88x31"),
	(13, "Micro Button | 80x15"),
	(14, "Vertical Banner | 120x240"),
	(15, "Square Button | 125x125"),
	(16, "Skyscraper | 120x600"),
	(17, "Wide Skyscraper | 160x600"),
	(18, "Half-Page | 300x600")
)


class Position(models.Model):

	name = models.CharField(max_length=255) 

	slug = models.CharField(max_length=255) 

	size = models.IntegerField(choices=STANDARD_AD_SIZES, default=0)

	width = models.IntegerField(default=0, null=False, blank=False, help_text="Use zero for unknown/variable values")
	
	height = models.IntegerField(default=0, null=False, blank=False, help_text="Use zero for unknown/variable values")

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
	
	url = models.URLField(null=True, blank=True, help_text="Click tag link")
	
	image = models.ImageField(null=True, blank=True, upload_to=UPLOAD_PATH + "custom_ads", help_text="Image for custom ad")
	
	embed = RichTextField(null=True, blank=True)

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
	
	attributes = {}
	_tile = 0
	disable_ad_manager = False

	def __init__(self, settings={}, site=None, zone=None, disable_ad_manager=None, *args, **kwargs):

		for setting in settings:
			self.__setattr__(setting, settings[setting])
			
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

		formatted = ''
		index = ''
		for val in values:
			enumerated_attr = attr + str(index)
			formatted += self._format_value(enumerated_attr, val)

			if index == '':
				index = 1
				
			index += 1

		return formatted
	
	
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

		# if ad manager is disabled, it goes straight to displaying the iframe/js code		
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
				# Check for a custom ad, otherwise load the DART code
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
