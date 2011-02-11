from coffin import template
from dart.ads import Ad

register = template.Library()

def get_ad(**kwargs):
	return Ad(**kwargs)

register.object(get_ad)