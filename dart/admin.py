from django.contrib import admin
from settings import ADMIN_MEDIA_PREFIX
from dart.models import Zone, Position, Custom_Ad, Zone_Position
from django.core.urlresolvers import reverse
from django.utils.functional import lazy

class Zone_PositionInline(admin.TabularInline):
    model = Zone.position.through


class Zone_Admin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ('name',)}
	css = {
		'all': (
			ADMIN_MEDIA_PREFIX + 'blog/css/autocomplete.css',
		)
	}
	
	fieldsets = (
		(None, {
			'fields': (
				'name',
				'slug',
			)
		}),
	)
	inlines = [
        Zone_PositionInline,
    ]


reverse_lazy = lazy(reverse, str)

class Position_Admin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ('name',)}
	
	class Media:
		
		js = (
			reverse_lazy("dart_static", args=("position.js",)),
				
		)
	
	fieldsets = (
		(None, {
			"fields": ("name", "slug", "size", )
		}),
		("Size", {
			"classes": ("collapse closed sizes",),
			"fields": ("width", "height")
		}),
	)
	
class Custom_Ad_Admin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			"fields": ("name", )
		}),
		("Image/URL", {
			"description": "Upload an image and a URL for a simple linked image ad unit",
			"classes": ("collapse closed sizes",),
			"fields": ("url", "image")
		}),
		
		("Custom Code", {
			"description": "Use this section to write custom HTML that would not otherwise be covered by the image/URL format. Overrides anything set in the image/URL section.",
			"classes": ("collapse closed sizes",),
			"fields": ("embed",)
		}),
	)

admin.site.register(Zone, Zone_Admin)
admin.site.register(Custom_Ad, Custom_Ad_Admin)
admin.site.register(Position, Position_Admin)