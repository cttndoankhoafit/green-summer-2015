# -*- coding: utf-8 -*-

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from mms_base.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(OrganizationType)
admin.site.register(Organization)
admin.site.register(OrganizationUser)
admin.site.register(ActivityType)
admin.site.register(Activity)
admin.site.register(ActivityUser)
admin.site.register(Period)
