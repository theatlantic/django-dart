from django import template
from django.template.defaultfilters import stringfilter
from dart.ads import Ad

register = template.Library()

@register.filter
@stringfilter
def ad_tag(value):

    def get_key_val(x):
        a = x.split('=')
        a = map(str, a) # Force string
        return a

    ad_attributes = dict(map(get_key_val, value.split(' ')))

    return Ad(**ad_attributes)