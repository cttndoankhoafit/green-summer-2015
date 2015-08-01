from django.conf.urls import include, url

from mms_crowler.views import *

urlpatterns = [
	url(r'^import/user/$', UserImportView.as_view(), name='crowler_user_import_view'),

	url(r'^import/organization_type/$', OrganizationTypeImportView.as_view(), name='crowler_organization_type_import_view'),

	url(r'^import/organization/$', OrganizationImportView.as_view(), name='crowler_organization_import_view'),

	url(r'^import/activity_type/$', ActivityTypeImportView.as_view(), name='crowler_activity_type_import_view'),

	url(r'^import/activity/$', ActivityImportView.as_view(), name='crowler_activity_import_view'),
	
	url(r'^import/activity_user/$', ActivityUserImportView.as_view(), name='crowler_activity_user_import_view'),
]