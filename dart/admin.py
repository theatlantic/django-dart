from django.contrib import admin

from dart.models import AdSections, AdPositions, AdSectionPositions

class AdSectionsAdmin(admin.ModelAdmin):
	pass

class AdPositionsAdmin(admin.ModelAdmin):
	pass
	
class AdSectionPositionsAdmin(admin.ModelAdmin):
	pass

admin.site.register(AdSections, AdSectionsAdmin)
admin.site.register(AdSectionPositions, AdSectionPositionsAdmin)
admin.site.register(AdPositions, AdPositionsAdmin)