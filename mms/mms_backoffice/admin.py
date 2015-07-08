# -*- coding: utf-8 -*-

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from mms_backoffice.models import *
from mms_backoffice.resources import *

class OrganizationImportExportModelAdmin(ImportExportModelAdmin):
	resource_class = OrganizationResource

class OrganizationTypeImportExportModelAdmin(ImportExportModelAdmin):
	resource_class = OrganizationTypeResource

class MemberImportExportModelAdmin(ImportExportModelAdmin):
	resource_class = MemberResource


# Register your models here.
admin.site.register(OrganizationType, OrganizationTypeImportExportModelAdmin)
admin.site.register(Organization, OrganizationImportExportModelAdmin)
admin.site.register(Member, MemberImportExportModelAdmin)