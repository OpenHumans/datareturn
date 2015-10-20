from django.contrib import admin

from datareturn.models import (DataFile, DataLink, OpenHumansConfig,
                               OpenHumansUser, SiteConfig)


admin.site.register(DataFile)
admin.site.register(DataLink)
admin.site.register(OpenHumansConfig)
admin.site.register(OpenHumansUser)
admin.site.register(SiteConfig)
