from django.conf.urls import include, url

from mms_webapp_v1.views.organization_type import *
from mms_webapp_v1.views.organization import *
from mms_webapp_v1.views.organization_temporary.views import *
from mms_webapp_v1.views.user import *
from mms_webapp_v1.views.member_temporary.views import *


from mms_webapp_v1.views.auth import LoginView, LogoutView
from mms_webapp_v1.views.dashboard import DashboardView

# from mms_webapp_v1.views.activity import ActivityListView

from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^login/$', LoginView.as_view(), name='login_v1'),
	url(r'^logout/$', LogoutView.as_view(), name='logout_v1'),

	url(r'^$', login_required(DashboardView.as_view()), name='dashboard_v1'),

	url(r'^profile/', login_required(UserProfileView.as_view()), name='user_profile_view_v1'),

	url(r'^user/(?P<user_identify>\d+)/$', login_required(UserUpdateView.as_view()), name='user_update_view_v1'),
	
	url(r'^user/', UserListView.as_view(), name='member_list_view_v1'),

	url(r'^member/', MemberListView.as_view(), name='member_list_view_v1'),

	url(r'^organization_type/$', OrganizationTypeListView.as_view(), name='organization_type_list_view_v1'),
	url(r'^organization_type/create/', OrganizationTypeCreateView.as_view(), name='organization_type_create_view_v1'),
	url(r'^organization/(?P<organization_id>\d+)/under_organization/$', OrganizationOrganizationView.as_view(), name='organization_organization_view_v1'),
	url(r'^user/(?P<user_id>[0-9]+)/organization/$', UserOrganizationView.as_view(), name='user_organization_view_v1'),
	url(r'^user/(?P<user_id>[0-9]+)/member/$', UserMemberListView.as_view(), name='user_member_list_view'),
	url(r'^organization/(?P<organization_id>\d+)/member/$', OrganizationMemberListView.as_view(), name='organization_member_list_view'),
]