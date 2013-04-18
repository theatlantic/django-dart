from random import randint
from urllib import urlencode

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
    tile = None

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

    def get_tile(self):
        return self.tile

    def set_tile(self, value):
        self.tile = value

    def _parse_attributes(self, noscript=False):
        parsed_attributes = {}

        for key, value in self.attributes.iteritems():

            # We need to recast QuerySets into lists of strings.
            if isinstance(value, QuerySet):
                value = [str(x) for x in value]

                if noscript is True:
                    value = ",".join(value)

            parsed_attributes[key] = value

        return parsed_attributes

    def get_dict(self):
        """
        Get the specially formatted dict that will be transformed into an
        ad_slot definition.
        """
        attributes = self._parse_attributes()

        return ("ad-{0}".format(self.pos), {
                    'sizes': self.size,
                    'zone': "/{0}/{1}/{2}".format(self.dfp_id, self.site, self.zone),
                    'properties': attributes,
                    })

    def get_noscript(self):
        """
        Build the noscript url parameters.
        """
        attributes = self._parse_attributes()
        url_params = {
                "iu": "/{0}/{1}/{2}".format(self.dfp_id, self.site, self.zone),
                "sz": "|".join(["{0}x{1}".format(w, h) for w, h in self.size]),
                "t": "&".join(["{0}={1}".format(k,v) for k, v in attributes.iteritems()]),
                "tile": self.tile,
                "c": randint(0, 1000000000),
                }
        return urlencode(url_params)

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
    tile = 0

    def __init__(self, **kwargs):
        self.attributes = self.default_attributes.copy()
        self.set(**kwargs)

    def set(self, **kwargs):
        self.attributes.update(kwargs)

    def get(self, *args, **kwargs):
        self.tile += 1

        attr = self.attributes.copy()
        attr.update(kwargs)

        ad = Ad(*args, **attr)
        ad.set_tile(self.tile)

        ad_slot_key, ad_slot_def = ad.get_dict()
        self.ad_slots[ad_slot_key] = ad_slot_def

        return ad
