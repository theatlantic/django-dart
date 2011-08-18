from django.contrib import admin
from cities.settings import ADMIN_MEDIA_PREFIX
from dart.models import Zone, Position, Custom_Ad, Zone_Position

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

class Position_Admin(admin.ModelAdmin):
	prepopulated_fields = {"slug" : ('name',)}
	css = {
		'all': (
			ADMIN_MEDIA_PREFIX + 'blog/css/autocomplete.css',
		)
	}
	
class Custom_Ad_Admin(admin.ModelAdmin):
	pass

admin.site.register(Zone, Zone_Admin)
admin.site.register(Custom_Ad, Custom_Ad_Admin)
admin.site.register(Position, Position_Admin)