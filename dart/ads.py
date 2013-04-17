from random import randint

from django.template.defaultfilters import slugify

from coffin.template import Context
from coffin.template.loader import get_template

from django.conf import settings

DART_AD_DEFAULTS = getattr(settings, 'DART_AD_DEFAULTS', {})

if hasattr(DART_AD_DEFAULTS, 'site'):
    DEFAULT_SITE = DART_AD_DEFAULTS['site']
    del(DART_AD_DEFAULTS['site'])
else:
    DEFAULT_SITE = 'site'

if hasattr(DART_AD_DEFAULTS, 'zone'):
    DEFAULT_SITE = DART_AD_DEFAULTS['zone']
    del(DART_AD_DEFAULTS['zone'])
else:
    DEFAULT_ZONE = 'zone'

if hasattr(DART_AD_DEFAULTS, 'dfp_id'):
    DEFAULT_ID = DART_AD_DEFAULTS['dfp_id']
    del(DART_AD_DEFAULTS['dfp_id'])
else:
    DEFAULT_ID = None

class Ad(object):
    """ Base class for Ad and Ad_Factory, keeps track of assigned attributes """

    default_site = DEFAULT_SITE
    default_zone = DEFAULT_ZONE
    default_id = DEFAULT_ID

    def __init__(self, pos, size='0x0', desc_text='', template='ad.html',**kwargs):

        try:
            self.site = kwargs['site']
            del(kwargs['site'])
        except KeyError:
            self.site = self.default_site

        try:
            self.zone = kwargs['zone']
            del(kwargs['zone'])
        except KeyError:
            self.zone = self.default_zone

        try:
            self.dfp_id = kwargs['dfp_id']
            del(kwargs['dfp_id'])
        except:
            self.dfp_id = self.default_id


        self.desc_text = desc_text
        self.template = template

        self.attributes = {}
        self.attributes.update(kwargs)
        self.attributes['pos'] = pos
        self.attributes['sz'] = size

    def get_zone(self):
        return self._zone

    def set_zone(self, value):
        self._zone = slugify(value)

    zone = property(get_zone, set_zone)

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
        formatted = u''
        for val in values:
            formatted = u'%s%s' % (formatted, self._format_value(attr, val))
        return formatted

    def __unicode__(self):
        """ Prints out the Ad using the ad.html template """

        link = self.get_link()
        t = get_template(self.template)
        c = Context({
            'pos': self.attributes['pos'],
            'link': link,
            'dfp_id': '/%s' % self.dfp_id if self.dfp_id is not None else '',
            'desc_text': self.desc_text
        })
        return t.render(c)

class AdFactory(object):

    attributes = {}
    default_attributes = DART_AD_DEFAULTS

    def __init__(self, **kwargs):
        self.attributes = self.default_attributes.copy()
        self.set(**kwargs)


    def set(self, **kwargs):
        self.attributes.update(kwargs)

    def get(self, *args, **kwargs):

        attr = self.attributes.copy()
        attr.update(kwargs)

        ad = Ad(*args, **attr)

        return ad
