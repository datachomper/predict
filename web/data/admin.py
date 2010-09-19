from data.models import Box
from django.contrib import admin

class BoxAdmin(admin.ModelAdmin):
	pass

admin.site.register(Box, BoxAdmin)
