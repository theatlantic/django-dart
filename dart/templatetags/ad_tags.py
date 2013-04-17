from coffin import template
from dart.ads import Ad, AdFactory

register = template.Library()

def get_ad(**kwargs):
    return Ad(**kwargs)

register.object(get_ad)

def get_adfactory(**kwargs):
    return AdFactory(**kwargs)

register.object(get_adfactory)
