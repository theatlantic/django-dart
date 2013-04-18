import collections

from django.template.defaultfilters import slugify
from django.db.models.query import QuerySet

from coffin.template import Context
from coffin.template.loader import get_template

from django.conf import settings

DART_AD_DEFAULTS = getattr(settings, 'DART_AD_DEFAULTS', {})

# This sets DEFAULT_SITE, DEFAULT_ZONE, DEFAULT_DFP_ID
for DEFAULT_KEY in ['site', 'zone', 'dfp_id']:
    if hasattr(DART_AD_DEFAULTS, DEFAULT_KEY):
        globals()['DEFAULT_{0}'.format(DEFAULT_KEY.upper())] = DART_AD_DEFAULTS[DEFAULT_KEY]
        del(DART_AD_DEFAULTS[DEFAULT_KEY])
    else:
        globals()['DEFAULT_{0}'.format(DEFAULT_KEY.upper())] = DEFAULT_KEY

class AdException(Exception):
    pass

class Ad(object):
    """
    Contains all data for a specific ad unit.
    """

    default_site = DEFAULT_SITE
    default_zone = DEFAULT_ZONE
    default_dfp_id = DEFAULT_DFP_ID

    def __init__(self, pos, size=[[0,0]], desc_text='', template='ad.html',**kwargs):
        if size is [[0,0]]:
            raise AdException("Size must be defined in all ad units.")

        # Set site, zone, dfp_id.
        for key in ['site', 'zone', 'dfp_id']:
            try:
                setattr(self, key, kwargs[key])
                del(kwargs[key])
            except KeyError:
                setattr(self, key, getattr(self, 'default_{0}'.format(key)))

        self.desc_text = desc_text
        self.template = template

        self.attributes = {}
        self.attributes.update(kwargs)
        self.attributes["pos"] = pos

        self.pos = pos
        self.size = size

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

    def get_dict(self):
        """
        Get the specially formatted dict that will be transformed into an
        ad_slot definition.
        """
        attributes = {}
        for key, value in self.attributes.iteritems():

            # We need to cast all iterables into lists of strings.
            if isinstance(value, QuerySet):
                value = [str(x) for x in value]

            attributes[key] = value

        return ("ad-{0}".format(self.pos), {
                    'sizes': self.size,
                    'zone': "/{0}/{1}/{2}".format(self.dfp_id, self.site, self.zone),
                    'properties': attributes,
                    })

    def get_noscript(self):
        """
        Build the noscript string.
        """
        pass

    def __unicode__(self):
        """ Prints out the Ad using the ad.html template """

        t = get_template(self.template)
        c = Context({
            'pos': self.pos,
            'noscript': self.get_noscript()
        })
        return t.render(c)

class AdFactory(object):

    attributes = {}
    default_attributes = DART_AD_DEFAULTS
    ad_slots = {}

    def __init__(self, **kwargs):
        self.attributes = self.default_attributes.copy()
        self.set(**kwargs)

    def set(self, **kwargs):
        self.attributes.update(kwargs)

    def get(self, *args, **kwargs):

        attr = self.attributes.copy()
        attr.update(kwargs)

        ad = Ad(*args, **attr)
        ad_slot_key, ad_slot_def = ad.get_dict()
        self.ad_slots[ad_slot_key] = ad_slot_def

        return ad
