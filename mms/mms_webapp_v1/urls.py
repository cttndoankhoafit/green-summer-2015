from django.conf.urls import include, url

from mms_webapp_v1.views.organization_type import *
from mms_webapp_v1.views.organization import *
from mms_webapp_v1.views.organization_temporary.views import *
from mms_webapp_v1.views.member_temporary.views import *

from mms_webapp_v1.views.user import *
from mms_webapp_v1.views.activity import *
from mms_webapp_v1.views.activity_type import *

from mms_webapp_v1.views.auth import LoginView, LogoutView
from mms_webapp_v1.views.dashboard import DashboardView

from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import password_change, password_change_done

urlpatterns = [
	url(r'^login/$', LoginView.as_view(), name='login_v1'),

	url(r'^logout/$', LogoutView.as_view(), name='logout_v1'),

	url(r'^$', login_required(DashboardView.as_view()), name='dashboard_v1'),
	
	# Users management
	url(r'^profile/$', login_required(UserProfileView.as_view()), name='user_profile_view_v1'),

	url(r'^edit-profile/$', login_required(UserProfileUpdateView.as_view()), name='user_profile_update_view_v1'),
	
	url(r'^change-password/$', login_required(UserPasswordChangeView.as_view()), name='user_password_change_view_v1'),
	
	url(r'^user/(?P<user_id>\d+)/$', login_required(UserDetailView.as_view()), name='user_detail_view_v1'),

	url(r'^user/(?P<user_id>\d+)/edit/$', login_required(UserUpdateView.as_view()), name='user_update_view_v1'),

	url(r'^user/(?P<user_id>\d+)/reset-password/$', login_required(UserResetPasswordView.as_view()), name='user_reset_password_view_v1'),

	url(r'^user/list/', login_required(UserListView.as_view()), name='user_list_view_v1'),

	url(r'^user/import/', login_required(UserImportView.as_view()), name='user_import_view_v1'),

	url(r'^user/create/', login_required(UserCreateView.as_view()), name='user_create_view_v1'),

	#Organization management
	url(r'^organization/list/$', login_required(OrganizationListView.as_view()), name='organization_list_view_v1'),

	url(r'^organization/tree/$', login_required(OrganizationTreeView.as_view()), name='organization_tree_view_v1'),

	url(r'^organization/create/$', login_required(OrganizationCreateView.as_view()), name='organization_create_view_v1'),

	url(r'^organization/import/$', login_required(OrganizationImportView.as_view()), name='organization_import_view_v1'),

	url(r'^organization/management_import/$', login_required(OrganizationManagementImportView.as_view()), name='organization_management_import_view_v1'),
	
	url(r'^organization/(?P<organization_id>\d+)/$', login_required(OrganizationDetailView.as_view()), name='organization_detail_view_v1'),

	url(r'^organization/(?P<organization_id>\d+)/member/$', login_required(OrganizationMemberListView.as_view()), name='organization_member_list_view_v1'),

	url(r'^organization/(?P<organization_id>\d+)/member/import/$', login_required(OrganizationMemberImportView.as_view()), name='organization_member_import_view_v1'),

	url(r'^organization_type/$', login_required(OrganizationTypeListView.as_view()), name='organization_type_list_view_v1'),

	url(r'^organization_type/import/$', login_required(OrganizationTypeImportView.as_view()), name='organization_type_import_view_v1'),

	url(r'^organization/(?P<organization_id>\d+)/under_organization/$', login_required(UnderOrganizationTreeView.as_view()), name='under_organization_tree_view_v1'),	


	# Activity management
	url(r'^activity_type/$', login_required(ActivityTypeListView.as_view()), name='activity_type_list_view_v1'),

	url(r'^activity_type/import/$', login_required(ActivityTypeImportView.as_view()), name='activity_type_import_view_v1'),

	url(r'^activity/list/', login_required(ActivityListView.as_view()), name='activity_list_view_v1'),

	url(r'^activity/(?P<activity_id>\d+)/$', login_required(ActivityDetailView.as_view()), name='activity_detail_view_v1'),

	url(r'^activity/(?P<activity_id>\d+)/member/$', login_required(ActivityMemberListView.as_view()), name='activity_member_list_view_v1'),

	url(r'^activity/import/$', login_required(ActivityImportView.as_view()), name='activity_import_view_v1'),

	url(r'^activity/create/$', login_required(ActivityCreateView.as_view()), name='activity_create_view_v1'),

	url(r'^organization_type/create/', OrganizationTypeCreateView.as_view(), name='organization_type_create_view_v1'),


	# url(r'^activity/(?P<activity_id>\d+)/', login_required(ActivityUpdateView.as_view()), name='activity_update_view_v1'),

	# url(r'^user/(?P<user_id>[0-9]+)/organization/$', UserOrganizationView.as_view(), name='user_organization_view_v1'),
	# url(r'^user/(?P<user_id>[0-9]+)/member/$', UserMemberListView.as_view(), name='user_member_list_view'),
	# url(r'^user/(?P<user_id>[0-9]+)/activity/$', UserActivityListView.as_view(), name='user_activity_list_view'),

]