from django.conf.urls import include, url

from mms_webapp_v1.views.organization_type import *
from mms_webapp_v1.views.organization.views import *
from mms_webapp_v1.views.member import *

urlpatterns = [
	url(r'^member/', MemberListView.as_view(), name='member_list_view_v1'),
	url(r'^organization_type/create/', OrganizationTypeCreateView.as_view(), name='organization_type_create_v1'),
	url(r'^organization/(?P<organization_id>[0-9]+)/organization/$', ChildOrganizationListView.as_view(), name='ChildOrganizationListView'),
	url(r'^user/(?P<user_id>[0-9]+)/organization/$', ManagedOrganizationListView.as_view(), name='ManagedOrganizationListView'),
	
]