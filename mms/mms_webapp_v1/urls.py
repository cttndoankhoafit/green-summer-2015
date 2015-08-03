from django.conf.urls import include, url

from mms_webapp_v1.views.organization_type import *
from mms_webapp_v1.views.organization import *
from mms_webapp_v1.views.organization_temporary.views import *

from mms_webapp_v1.views.user import *
from mms_webapp_v1.views.activity import *
from mms_webapp_v1.views.activity_type import *
from mms_webapp_v1.views.yumt import *

from mms_webapp_v1.views.auth import LoginView, LogoutView
from mms_webapp_v1.views.dashboard import DashboardView

from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import password_change, password_change_done

urlpatterns = [
	url(r'^login/$', LoginView.as_view(), name='login_v1'),

	url(r'^logout/$', LogoutView.as_view(), name='logout_v1'),

	url(r'^$', login_required(DashboardView.as_view()), name='dashboard_v1'),
	
	# Users management
	# url(r'^change_password/$', login_required(UserPasswordChangeView.as_view()), name='user_password_change_view_v1'),
	
	url(r'^user/user=(?P<user_id>\w+)/$', login_required(UserDetailView.as_view()), name='user_detail_view_v1'),

	url(r'^user/user=(?P<user_id>\w+)/edit/$', login_required(UserUpdateView.as_view()), name='user_update_view_v1'),

	url(r'^user/user=(?P<user_id>\w+)/activity/$', login_required(UserActivityView.as_view()), name='user_activity_view_v1'),

	url(r'^user/user=(?P<user_id>\w+)/activity/period=(?P<period_id>\w+)/$', login_required(UserActivityView.as_view()), name='user_activity_period_view_v1'),

	url(r'^user/user=(?P<user_id>\w+)/change_password/$', login_required(UserPasswordChangeView.as_view()), name='user_password_change_view_v1'),

	url(r'^user/list/$', login_required(UserListView.as_view()), name='user_list_view_v1'),

	url(r'^user/import/$', login_required(UserImportView.as_view()), name='user_import_view_v1'),

	url(r'^user/create/$', login_required(UserCreateView.as_view()), name='user_create_view_v1'),

	#Organization management
	url(r'^organization/list/$', login_required(OrganizationListView.as_view()), name='organization_list_view_v1'),

	url(r'^organization/tree/$', login_required(OrganizationTreeView.as_view()), name='organization_tree_view_v1'),

	url(r'^organization/create/$', login_required(OrganizationCreateView.as_view()), name='organization_create_view_v1'),

	url(r'^organization/import/$', login_required(OrganizationImportView.as_view()), name='organization_import_view_v1'),
	
	url(r'^organization/organization=(?P<organization_id>\w+)/$', login_required(OrganizationDetailView.as_view()), name='organization_detail_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/edit/$', login_required(OrganizationUpdateView.as_view()), name='organization_update_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/permission/$', login_required(OrganizationPermissionListView.as_view()), name='organization_permission_list_view_v1'),



	url(r'^organization/organization=(?P<organization_id>\w+)/permission/create/$', login_required(OrganizationPermissionCreateView.as_view()), name='organization_permission_create_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/permission/import/$', login_required(OrganizationPermissionImportView.as_view()), name='organization_permission_import_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/permission/user=(?P<user_id>\w+)/$', login_required(OrganizationPermissionUpdateView.as_view()), name='organization_permission_update_view_v1'),





	url(r'^organization/organization=(?P<organization_id>\w+)/member/$', login_required(OrganizationMemberListView.as_view()), name='organization_member_list_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/member/import/$', login_required(OrganizationMemberImportView.as_view()), name='organization_member_import_view_v1'),


	# url(r'^organization/organization=(?P<organization_id>\w+)/member/statistics/$', login_required(OrganizationMemberStatisticsView.as_view()), name='organization_member_statistics_view_v1'),

	
	url(r'^organization/organization=(?P<organization_id>\w+)/activity/$', login_required(OrganizationActivityListView.as_view()), name='organization_activity_list_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/activity/import/$', login_required(OrganizationActivityImportView.as_view()), name='organization_activity_import_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/activity/create/$', login_required(OrganizationActivityCreateView.as_view()), name='organization_activity_create_view_v1'),


	url(r'^organization/organization=(?P<organization_id>\w+)/tree/$', login_required(ChildOrganizationTreeView.as_view()), name='child_organization_tree_view_v1'),	




	url(r'^organization_type/list/$', login_required(OrganizationTypeListView.as_view()), name='organization_type_list_view_v1'),

	url(r'^organization_type/import/$', login_required(OrganizationTypeImportView.as_view()), name='organization_type_import_view_v1'),

	url(r'^organization_type/create/$', login_required(OrganizationTypeCreateView.as_view()),name='organization_type_create_view_v1'),

	url(r'^organization_type/organization_type=(?P<organization_type_id>\w+)/edit/$', login_required(OrganizationTypeUpdateView.as_view()),name='organization_type_update_view_v1'),

	
	
	

	# Activity management
	url(r'^activity_type/list/$', login_required(ActivityTypeListView.as_view()), name='activity_type_list_view_v1'),

	url(r'^activity_type/create/$', login_required(ActivityTypeCreateView.as_view()), name='activity_type_create_view_v1'),


	url(r'^activity_type/import/$', login_required(ActivityTypeImportView.as_view()), name='activity_type_import_view_v1'),




	url(r'^activity/list/$', login_required(ActivityListView.as_view()), name='activity_list_view_v1'),

	url(r'^activity/list/organization=(?P<organization_id>\w+)/$$', login_required(ActivityListView.as_view()), name='activity_organization_list_view_v1'),

	url(r'^activity/activity=(?P<activity_id>\w+)/$', login_required(ActivityDetailView.as_view()), name='activity_detail_view_v1'),

	url(r'^activity/activity=(?P<activity_id>\w+)/member/$', login_required(ActivityMemberListView.as_view()), name='activity_member_list_view_v1'),


	url(r'^activity/activity=(?P<activity_id>\w+)/member/import/$', login_required(ActivityMemberImportView.as_view()), name='activity_member_import_view_v1'),


	url(r'^activity/activity=(?P<activity_id>\w+)/edit/$', login_required(ActivityUpdateView.as_view()), name='activity_update_view_v1'),

	url(r'^activity/activity=(?P<activity_id>\w+)/permission/$', login_required(ActivityPermissionListView.as_view()), name='activity_permission_list_view_v1'),


	url(r'^activity/activity=(?P<activity_id>\w+)/permission/create/$', login_required(ActivityPermissionCreateView.as_view()), name='activity_permission_create_view_v1'),

	url(r'^activity/activity=(?P<activity_id>\w+)/permission/user=(?P<user_id>\w+)/$', login_required(ActivityPermissionUpdateView.as_view()), name='activity_permission_update_view_v1'),

	url(r'^activity/activity=(?P<activity_id>\w+)/permission/import/$', login_required(ActivityPermissionImportView.as_view()), name='activity_permission_import_view_v1'),



	
	url(r'yumt/register/$', login_required(YUMTRegisterView.as_view()), name='yumt_register_view_v1'),

]