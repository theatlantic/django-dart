from django.db import models
from blogstract.status import ACTIVE_STATUS, Status
from cropduster.models import CropDusterField
from django.template.defaultfilters import slugify

from coffin.template import Context, loader

from settings import DART_AD_DEFAULTS

AD_STATES = (
	(1, 'Hard-coded'),
	(Status.SCHEDULED, 'On'),
	(Status.PUBLISHED, 'Off'),
)

class AdSections(models.Model):

	name = models.CharField(max_length=765) 

	zone = models.CharField(max_length=765) 


	class Meta:
		db_table = u'ad_sections'
		verbose_name = 'Ad Section'
		verbose_name_plural = 'Ad Sections'
		
	def __unicode__(self):
		return u'%s' % self.name

class AdPositions(models.Model):

	name = models.CharField(max_length=255) 

	slug = models.CharField(max_length=255) 

	size = models.CharField(max_length=255)

	class Meta:
		db_table = u'ad_positions'
		verbose_name = 'Ad Position'
		verbose_name_plural = 'Ad Positions'
		
	def __unicode__(self):
		return u'%s' % self.name	
		
class AdSectionPositions(models.Model):

	name = models.CharField(max_length=255) 

	section = models.ForeignKey(AdSections, 
		db_column='section_id',
		null=True)

	position = models.ForeignKey(AdPositions, 
		db_column='position_id',
		null=True)

	state = models.IntegerField(choices=(
		(1,'Hard Coded'),
		(2,'On'),
		(3,'Off')
	), default=1, db_index=True)

	url = models.URLField(blank=True, verify_exists=False) 

	class Meta:
		db_table = u'ad_section_positions'
		verbose_name = 'Ad'
		verbose_name_plural = 'Ads'
		
	def __unicode__(self):
		return u'%s' % self.name
		
class AdSectionPositionImages(models.Model):

	section_position = models.ForeignKey(AdSectionPositions, 
		db_column='section_position_id',
		null=True)

	_image = CropDusterField(
		null=True,
		blank=True,
		db_column='image_id'
	)
	__image = False

	active = models.IntegerField(choices=ACTIVE_STATUS, default=1) 

	class Meta:
		db_table = u'ad_section_position_images'
		verbose_name = 'Ad Images'
		verbose_name_plural = 'Ad Images'
		

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