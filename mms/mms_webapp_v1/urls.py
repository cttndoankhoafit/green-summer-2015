from mms_webapp_v1.views.organization_type import *

from django.conf.urls import include, url

urlpatterns = [
	url(r'^organization_type/create/', OrganizationTypeCreateView.as_view(), name='organization_type_create_v1'),
	url(r'^organization/(?P<organization_id>[0-9]+)/child-organizations/$', ChildOrganizationListView.as_view(), name='ChildOrganizationListView'),
    url(r'^user/(?P<user_id>[0-9]+)/managed-organizations/$', ManagedOrganizationListView.as_view(), name='ManagedOrganizationListView'),
]