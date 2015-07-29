from django.conf.urls import include, url

from mms_webapp_v1.views.organization_type import *
from mms_webapp_v1.views.organization import *
from mms_webapp_v1.views.organization_temporary.views import *

from mms_webapp_v1.views.user import *
from mms_webapp_v1.views.activity import *
from mms_webapp_v1.views.activity_type import *
from mms_webapp_v1.views.renluyendoanvien import *

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

	url(r'^user/user=(?P<user_id>\w+)/change_password/$', login_required(UserPasswordChangeView.as_view()), name='user_password_change_view_v1'),

	url(r'^user/list/$', login_required(UserListView.as_view()), name='user_list_view_v1'),

	url(r'^user/import/$', login_required(UserImportView.as_view()), name='user_import_view_v1'),

	url(r'^user/create/$', login_required(UserCreateView.as_view()), name='user_create_view_v1'),

	#Organization management
	url(r'^organization/list/$', login_required(OrganizationListView.as_view()), name='organization_list_view_v1'),

	url(r'^organization/tree/$', login_required(OrganizationTreeView.as_view()), name='organization_tree_view_v1'),

	url(r'^organization/create/$', login_required(OrganizationCreateView.as_view()), name='organization_create_view_v1'),

	url(r'^organization/import/$', login_required(OrganizationImportView.as_view()), name='organization_import_view_v1'),

	url(r'^organization/management_import/$', login_required(OrganizationManagementImportView.as_view()), name='organization_management_import_view_v1'),
	
	url(r'^organization/organization=(?P<organization_id>\w+)/$', login_required(OrganizationDetailView.as_view()), name='organization_detail_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/edit/$', login_required(OrganizationUpdateView.as_view()), name='organization_update_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/member/$', login_required(OrganizationMemberListView.as_view()), name='organization_member_list_view_v1'),

	url(r'^organization/organization=(?P<organization_id>\w+)/member/import/$', login_required(OrganizationMemberImportView.as_view()), name='organization_member_import_view_v1'),


	# url(r'^organization/organization=(?P<organization_id>\w+)/member/statistics/$', login_required(OrganizationMemberStatisticsView.as_view()), name='organization_member_statistics_view_v1'),

	
	url(r'^organization/organization=(?P<organization_id>\w+)/activity/list/$', login_required(OrganizationActivityListView.as_view()), name='organization_activity_list_view_v1'),

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

	url(r'^activity/activity=(?P<activity_id>\w+)/$', login_required(ActivityDetailView.as_view()), name='activity_detail_view_v1'),

	url(r'^activity/activity=(?P<activity_id>\w+)/member/$', login_required(ActivityMemberListView.as_view()), name='activity_member_list_view_v1'),

	url(r'^activity/activity=(?P<activity_id>\w+)/edit/$', login_required(ActivityUpdateView.as_view()), name='activity_update_view_v1'),


	url(r'^activity/import/$', login_required(ActivityImportView.as_view()), name='activity_import_view_v1'),

	url(r'^activity/create/$', login_required(ActivityCreateView.as_view()), name='activity_create_view_v1'),

	url(r'^activity/listonweek/$', login_required(ActivityListViewWeek.as_view()), name='activity_listonweek_view_v1'),

	url(r'^activity/filter/$', login_required(ActivityFilter.as_view()), name='activity_filter_view_v1'),
	#url(r'^activity/(?P<activity>\d+)/edit/$', login_required(ActivityUpdateView.as_view()), name='user_update_view_v1'), #phan moi

	# url(r'^organization_type/create/', OrganizationTypeCreateView.as_view(), name='organization_type_create_view_v1'),

	
	# url(r'^activity/(?P<activity_id>\d+)/', login_required(ActivityUpdateView.as_view()), name='activity_update_view_v1'),

	# url(r'^user/(?P<user_id>[0-9]+)/organization/$', UserOrganizationView.as_view(), name='user_organization_view_v1'),
	# url(r'^user/(?P<user_id>[0-9]+)/member/$', UserMemberListView.as_view(), name='user_member_list_view'),
	# url(r'^user/(?P<user_id>[0-9]+)/activity/$', UserActivityListView.as_view(), name='user_activity_list_view'),

	url(r'^renluyendoanvien/tudanhgia/$', login_required(RenLuyenDoanVien_TuDanhGia_ListView.as_view()), name='renluyendoanvien_tudanhgia_view_v1'),
	url(r'^renluyendoanvien/ketquadanhgia/$', login_required(RenLuyenDoanVien_KetquaDanhGia_ListView.as_view()), name='renluyendoanvien_ketquadanhgia_view_v1'),
	url(r'^renluyendoanvien/danhgiadoanvien/user=(?P<user_id>\w+)$', login_required(RenLuyenDoanVien_DanhGiaDoanVien_ListView.as_view()), name='renluyendoanvien_danhgiadoanvien_view_v1'),

]