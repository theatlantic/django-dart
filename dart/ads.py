import collections
import json
import re

from random import randint
from urllib import urlencode

from django.template.defaultfilters import slugify

from coffin.template import Context
from coffin.template.loader import get_template

from django.conf import settings

DART_AD_DEFAULTS = getattr(settings, 'DART_AD_DEFAULTS', {})


class AdException(Exception):
    pass


class Ad(object):
    """
    Contains all data for a specific ad unit.
    """
    tile = None

    def __init__(self, pos, size=[[0, 0]], desc_text='', template='dart/ad.html', **kwargs):
        if size is [[0, 0]]:
            raise AdException("Size must be defined in all ad units.")
        elif isinstance(size, basestring):
            try:
                size = Ad._parse_sizes(size)
            except AdException:
                # The ad won't work but we don't want to explode the entire
                # page for one mistake.
                size = None

        # Set site, zone, dfp_id.
        for key in ['site', 'zone', 'dfp_id']:
            try:
                setattr(self, key, kwargs.pop(key))
            except KeyError:
                setattr(self, key, DART_AD_DEFAULTS[key])

        self.desc_text = desc_text
        self.template = template

        # There are a couple special cases that are not GPT 'properties'
        #  - 'callbacks' is a list of JS methods to be called when an ad is
        #    rendered.
        #  - 'cookie' tells the GPT processor to check for a cookie before
        #    creating the slot definition
        for special_case in ['callbacks', 'cookie']:
            if special_case in kwargs:
                setattr(self, special_case, kwargs.pop(special_case))

        self.attributes = {}
        self.attributes.update(kwargs)
        self.attributes["pos"] = pos

        self.pos = pos
        self.size = size

    @property
    def zone(self):
        return self._zone

    @zone.setter
    def zone(self, value):
        """ We need to slugify the zone but preserve slashes. """
        slugified_values = []
        if isinstance(value, basestring):
            parts = value.split("/")
        else:
            parts = value

        for part in parts:
            slugified_values.append(slugify(part))

        self._zone = "/".join(slugified_values)

    def _parse_attributes(self, noscript=False):
        parsed_attributes = {}

        for key, value in self.attributes.iteritems():

            # Attributes need to be handled in different ways if they're lists.
            if not value:
                continue
            elif isinstance(value, basestring):
                value = slugify(value)
            elif isinstance(value, collections.Mapping):
                raise AdException("Mappings are not allowed in properties.")
            else:
                try:
                    value = [slugify(x) for x in value]
                except TypeError:
                    value = slugify(value)

            parsed_attributes[key] = value

        return parsed_attributes

    @staticmethod
    def _parse_sizes(sizes):
        try:
            sizes = json.loads(sizes)
        except ValueError:
            sizes = sizes.replace(" ", "")
            matches = re.search(r'^(?:(\d+x\d+),)*(\d+x\d+)$', sizes)

            if not matches:
                raise AdException("Size string is not in the correct form.")
            else:
                sizes = [[int(x) for x in size.split("x")] for size in
                         sizes.split(",")]
        return sizes

    @staticmethod
    def is_valid_size(sizes):
        try:
            sz = Ad._parse_sizes(sizes)
        except AdException:
            return False
        return bool(sz)

    def get_dict(self):
        """
        Get the specially formatted dict that will be transformed into an
        ad_slot definition.
        """
        attributes = self._parse_attributes()
        json_dict = {'sizes': self.size,
            'zone': "/{0}/{1}/{2}".format(self.dfp_id, self.site, self.zone),
            'properties': attributes, }

        if hasattr(self, 'cookie') and settings.DEBUG is False:
            json_dict['cookie'] = self.cookie

        return ("ad-{0}".format(self.pos), json_dict)

    def get_noscript(self):
        """
        Build the noscript url parameters.

         - iu is the zone
         - sz needs to be in the form of 000x000|111x111|...
         - t needs to be a url encoded string of url parameters.
         - tile is an identifier of the adslot on the page.
         - c is a cache buster.
        """
        attributes = self._parse_attributes()
        url_params = {
                "iu": "/{0}/{1}/{2}".format(self.dfp_id, self.site, self.zone),
                "sz": "|".join(["{0}x{1}".format(w, h) for w, h in self.size]),
                "t": "&".join(["{0}={1}".format(k, v) for k, v in attributes.iteritems()]),
                "tile": self.tile,
                "c": randint(0, 1000000000),
                }
        return urlencode(url_params)

    def __unicode__(self):
        """ Prints out the Ad using the ad.html template """

        t = get_template(self.template)
        c = Context({
            'pos': self.pos,
            'noscript': self.get_noscript(),
            'callbacks': self.callbacks if hasattr(self, 'callbacks') else None,
            'desc_text': self.desc_text,
        })
        return t.render(c)


class AdFactory(object):

    attributes = {}
    default_attributes = DART_AD_DEFAULTS
    page_vars = {}
    _ad_slots = None
    _ads = None
    tile = 0

    def __init__(self, **kwargs):
        """
        Initialize the AdFactory with default options that should be set on
        each ad.

        Use the kwarg `page_vars` to set page-wide properties. All other
        kwargs will be passed to each ad.

        Ideally, everything set on factory would be global. This is a quick fix
        to enable it without breaking the API.

        """
        self._ad_slots = {}
        self._ads = {}

        if 'page_vars' in kwargs:
            self.page_vars = kwargs.pop('page_vars')

        self.attributes = self.default_attributes.copy()
        self.set(**kwargs)

    def get_page_properties(self):
        """ Gets the page-level paramters as JSON. """
        page_vars = self.page_vars
        for key, val in page_vars.items():
            self.page_vars[key] = slugify(val)
        return json.dumps(self.page_vars)

    @property
    def ad_slots(self):
        return json.dumps(self._ad_slots)

    def define(self, pos, **kwargs):
        """
        Add a slot definition. This allows us to cache them so we can access
        them later.
        """
        if not pos:
            return

        self.tile += 1

        attr = self.attributes.copy()
        attr.update(kwargs)

        ad = Ad(pos, **attr)
        ad.tile = self.tile

        ad_slot_key, ad_slot_def = ad.get_dict()
        self._ad_slots[ad_slot_key] = ad_slot_def
        self._ads[ad_slot_key] = ad
        return ad

    def set(self, **kwargs):
        self.attributes.update(kwargs)

    def get(self, pos, *args, **kwargs):
        """
        Retreive a slot definition if it exists. Otherwise, create it.

        If a slot already exists, it will not be updated.
        """
        if "ad-{0}".format(pos) not in self._ads:
            ad = self.define(pos, **kwargs)
        else:
            ad = self._ads["ad-{0}".format(pos)]

        return ad
