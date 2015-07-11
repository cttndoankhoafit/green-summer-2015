from django.conf.urls import include, url

from mms_webapp_v1.views.organization_type import *
from mms_webapp_v1.views.organization import *
from mms_webapp_v1.views.organization_temporary.views import *
from mms_webapp_v1.views.member import *
from mms_webapp_v1.views.member_temporary.views import *

urlpatterns = [
	url(r'^member/', MemberListView.as_view(), name='member_list_view_v1'),
	url(r'^organization_type/$', OrganizationTypeListView.as_view(), name='organization_type_list_view_v1'),
	url(r'^organization_type/create/', OrganizationTypeCreateView.as_view(), name='organization_type_create_view_v1'),
	url(r'^organization/(?P<organization_id>\d+)/under_organization/$', OrganizationOrganizationView.as_view(), name='organization_organization_view_v1'),
	url(r'^user/(?P<user_id>[0-9]+)/organization/$', UserOrganizationView.as_view(), name='user_organization_view_v1'),
	url(r'^user/(?P<user_id>[0-9]+)/member/$', UserMemberListView.as_view(), name='user_member_list_view'),
	url(r'^organization/(?P<organization_id>\d+)/member/$', OrganizationMemberListView.as_view(), name='organization_member_list_view'),
]