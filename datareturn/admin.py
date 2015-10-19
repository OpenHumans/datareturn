from django.contrib import admin

from datareturn.models import DataFile, DataLink, SiteConfig


admin.site.register(DataFile)
admin.site.register(DataLink)
admin.site.register(SiteConfig)
