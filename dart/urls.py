from coffin.conf.urls.defaults import *

urlpatterns = patterns('dart.views',
	url(r'^(?P<ad_url>\S+)$', 'ad'),
)
