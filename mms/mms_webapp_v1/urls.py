from mms_webapp_v1.views.organization_type import *

from django.conf.urls import include, url

urlpatterns = [
	url(r'^organization_type/create/', OrganizationTypeCreateView.as_view(), name='organization_type_create_v1'),
]
