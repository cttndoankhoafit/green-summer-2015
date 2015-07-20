from django.conf.urls import include, url

from mms_webapp_v1.views.organization_type import *
from mms_webapp_v1.views.organization import *
from mms_webapp_v1.views.organization_temporary.views import *
from mms_webapp_v1.views.member_temporary.views import *

from mms_webapp_v1.views.user import *
from mms_webapp_v1.views.activity import *

from mms_webapp_v1.views.auth import LoginView, LogoutView
from mms_webapp_v1.views.dashboard import DashboardView

from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import password_change, password_change_done

urlpatterns = [
	url(r'^login/$', LoginView.as_view(), name='login_v1'),

	url(r'^logout/$', LogoutView.as_view(), name='logout_v1'),

	url(r'^$', login_required(DashboardView.as_view()), name='dashboard_v1'),

	# url(r'^profile/edit/$', login_required(UserUpdateProfileView.as_view()), name='user_update_profile_view_v1'),
	
	url(r'^profile/$', login_required(UserProfileView.as_view()), name='user_profile_view_v1'),

	url(r'^edit-profile/$', login_required(UserProfileUpdateView.as_view()), name='user_profile_update_view_v1'),

	url(r'^change-password-done/$', 'django.contrib.auth.views.password_change_done', kwargs={'template_name': 'v1/user/change_password_done.html'}, name='user_change_password_done_v1'),

	url(r'^change-password/$', 'django.contrib.auth.views.password_change', kwargs={'post_change_redirect' : '/change-password-done/', 'template_name': 'v1/user/change_password.html'}, name='user_change_password_v1'),
	
	url(r'^user/(?P<user_id>\d+)/$', login_required(UserDetailView.as_view()), name='user_detail_view_v1'),

	url(r'^user/(?P<user_id>\d+)/edit/$', login_required(UserUpdateView.as_view()), name='user_update_view_v1'),

	url(r'^user/(?P<user_id>\d+)/reset-password/$', login_required(UserResetPasswordView.as_view()), name='user_reset_password_view_v1'),

	url(r'^user/(?P<user_id>\d+)/reset-password-done/$', login_required(UserResetPasswordDoneView.as_view()), name='user_reset_password_done_view_v1'),

	url(r'^user/list/', login_required(UserListView.as_view()), name='user_list_view_v1'),

	url(r'^user/import/', login_required(UserImportView.as_view()), name='user_import_view_v1'),

	url(r'^user/import/', login_required(UserProcessImportView.as_view()), name='user_process_import_view_v1'),

	url(r'^user/create/', login_required(UserCreateView.as_view()), name='user_create_view_v1'),

	url(r'^activity/list/', login_required(ActivityListView.as_view()), name='activity_list_view_v1'),

	url(r'^activity/(?P<activity_id>\d+)/', login_required(ActivityUpdateView.as_view()), name='activity_update_view_v1'),



	# url(r'^member/', MemberListView.as_view(), name='member_list_view_v1'),

	url(r'^organization_type/$', OrganizationTypeListView.as_view(), name='organization_type_list_view_v1'),
	url(r'^organization_type/create/', OrganizationTypeCreateView.as_view(), name='organization_type_create_view_v1'),
	url(r'^organization/create/$', OrganizationCreateView.as_view(), name='organization_create_view'),
	url(r'^organization/(?P<organization_id>\d+)/under_organization/$', OrganizationOrganizationView.as_view(), name='organization_organization_view_v1'),
	url(r'^user/(?P<user_id>[0-9]+)/organization/$', UserOrganizationView.as_view(), name='user_organization_view_v1'),
	url(r'^user/(?P<user_id>[0-9]+)/member/$', UserMemberListView.as_view(), name='user_member_list_view'),
	url(r'^user/(?P<user_id>[0-9]+)/activity/$', UserActivityListView.as_view(), name='user_activity_list_view'),
	url(r'^user/create/$', UserCreateView.as_view(), name='user_create_view'),
	url(r'^organization/(?P<organization_id>\d+)/member/$', OrganizationMemberListView.as_view(), name='organization_member_list_view'),


]