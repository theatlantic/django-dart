from coffin.conf.urls.defaults import *
import os

urlpatterns = patterns('dart.views',
	url(r'^(?P<ad_url>\S+)$', 'ad'),
	
	url(r"^media/(?P<path>.*)$", "django.views.static.serve", {"document_root": os.path.dirname(__file__) + "/media"}, "dart_static"),
)
