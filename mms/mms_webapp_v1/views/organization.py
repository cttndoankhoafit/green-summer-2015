# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.utils.html import mark_safe

from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView

from django.http import HttpResponseRedirect, HttpResponse, Http404

from django.core.urlresolvers import reverse_lazy, reverse

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_webapp_v1.forms.organization import *

from mms_webapp_v1.views.bases.base_view import *

from mms_base.resources import *



# Khung nhìn chung cho việc xem thông tin của một tổ chức
class BaseOrganizationView(BaseView):

	def get_organization_id(self):
		return self.kwargs['organization_id']

	def get_context_data(self, **kwargs):
		context = super(BaseOrganizationView, self).get_context_data(**kwargs)

		context['page_title'] = get_organization_model().objects.get(identify=self.get_organization_id()).name
		context['organization_id'] = self.get_organization_id()

		if is_organization_administrator(self.get_user_id(), self.get_organization_id()):
			context['organization_administrator'] = 1

		if is_organization_manager(self.get_user_id(), self.get_organization_id()):
			context['organization_manager'] = 1

		return context



# Khung nhìn xem thông tin của tổ chức
class OrganizationDetailView(BaseOrganizationView, TemplateView):
	template_name = 'v1/organization/profile/overview.html'

	def get_context_data(self, **kwargs):
		context = super(OrganizationDetailView, self).get_context_data(**kwargs)
		context['overview_active'] ='active'

		organization_object = get_organization(self.get_organization_id())

		context['organization_type'] = organization_object.organization_type
		context['management_organization'] = mark_safe(u'<a href="/organization/organization=%s">%s</a>' % (organization_object.management_organization.identify, organization_object.management_organization.name)) 
		context['description'] = organization_object.description

		context['staff_list'] = self.get_staff()

		return context

	def get_staff(self):
		organization_staff_list = get_organization_staff(self.get_organization_id())

		objects = []
		for obj in organization_staff_list:
			objects.append({ 'name' : obj.user.get_full_name(), 'position' : obj.position.name })

		return objects



# Khung nhìn chung quản lý danh sách hoạt động của tổ chức
class BaseOrganizationActivityView(BaseOrganizationView):

	can_set = 0

	def get_context_data(self, **kwargs):
		context = super(BaseOrganizationActivityView, self).get_context_data(**kwargs)

		if is_organization_manager(self.get_user_id(), self.get_organization_id()):
			self.can_set = 1
			context['can_set'] = 'active'

		return context



# Khung nhìn xem danh sách hoạt động của tổ chức
class OrganizationActivityListView(BaseOrganizationActivityView, ListView):
	template_name = 'v1/organization/profile/activity/list.html'
	paginate_by = '20'
 
	def get_context_data(self, **kwargs):
		context = super(OrganizationActivityListView, self).get_context_data(**kwargs)
		
		org = get_organization_root()
		
		context['theads'] = [	{'name': u'#', 'size' : '10%'},
								{'name': u'Tên hoạt động', 'size' : 'auto'},	]

		context['activities_active'] ='active'

		context['import_link'] = 'import/'

		if self.can_set:
			context['show_add_button'] = 1
			context['show_delete_button'] = 1
			context['show_import_button'] = 1
			context['show_checkbox'] = 1
			context['show_statistics_button'] = 1

		return context

	def get_queryset(self):
		activity_list = get_organization_activity_list(self.get_organization_id())

		objects = []

		can_set = is_organization_manager(self.get_user_id(), self.get_organization_id())

		for obj in activity_list:
			values = []
			if can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="%s" name="list"/>' % obj.identify))
			values.append(obj.identify)
			values.append(mark_safe(u'<a href="/activity/activity=%s">%s</a>' % (obj.identify, obj.name)))
			objects.append(values)

		return objects



# Khung nhìn nhập danh sách hoạt động trong tổ chức
class OrganizationActivityImportView(BaseOrganizationActivityView, BaseImportView):
	template_name = 'v1/organization/profile/activity/import.html'

	CONST_FIELDS = ('identify',	'name',	'type')

	def get_context_data(self, **kwargs):
		if not is_organization_manager(self.get_user_id(), self.get_organization_id()):
			raise PermissionDenied

		context = super(OrganizationActivityImportView, self).get_context_data(**kwargs)
		
		context['activities_active'] ='active'

		return context

	def get_success_url(self):
		return reverse('organization_activity_list_view_v1', kwargs={ 'organization_id' : self.get_organization_id() })

	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False

		activity_identify = row['identify']
		activity_name = row['name']
		activity_type = row['type']

		if set_organization_activity(self.get_user_id(), self.get_organization_id(), activity_identify, activity_name, activity_type):
			print 'Import activity ' + activity_identify + ' to ' + self.get_organization_id() + ' complete'
			print '----------'
			return True

		return False



# Khung nhìn tạo hoạt động cho một tổ chức
class OrganizationActivityCreateView(BaseOrganizationActivityView, BaseSuccessMessageMixin, CreateView):
	model = Activity

	template_name = 'v1/organization/profile/activity/create.html'

	success_message = u'Thêm hoạt động thành công'

	fields =[	'identify',
				'name',
				'activity_type',
				'description',
				'start_time',
				'end_time',
				'credits',
				'score',
				'register_start_time',
				'register_end_time',
				'register_state',
				'published'	]

	def get_form(self, form_class):
		form = super(OrganizationActivityCreateView, self).get_form(form_class)

		form.fields['identify'].widget.attrs['class'] = 'form-control'
		form.fields['name'].widget.attrs['class'] = 'form-control'
		form.fields['activity_type'].widget.attrs['class'] = 'form-control'
		form.fields['description'].widget.attrs['class'] = 'form-control'
		form.fields['published'].widget.attrs['class'] = 'form-control'
		
		form.fields['start_time'].widget.attrs['class'] = 'form-control'
		form.fields['start_time'].widget.attrs['readonly'] = '1'
		
		form.fields['end_time'].widget.attrs['class'] = 'form-control'
		form.fields['end_time'].widget.attrs['readonly'] = '1'

		form.fields['credits'].widget.attrs['class'] = 'form-control'
		form.fields['score'].widget.attrs['class'] = 'form-control'

		form.fields['register_start_time'].widget.attrs['class'] = 'form-control'
		form.fields['register_start_time'].widget.attrs['readonly'] = '1'

		form.fields['register_end_time'].widget.attrs['class'] = 'form-control'
		form.fields['register_end_time'].widget.attrs['readonly'] = '1'

		form.fields['register_state'].widget.attrs['class'] = 'form-control'

		return form

	def get_success_url(self):
		return reverse('organization_activity_list_view_v1', kwargs={ 'organization_id' : self.get_organization_id() })

	def get_context_data(self, **kwargs):
		if not is_organization_manager(self.get_user_id(), self.get_organization_id()):
			raise PermissionDenied

		context = super(OrganizationActivityCreateView, self).get_context_data(**kwargs)
		
		context['activities_active'] ='active'

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.organization = get_organization(self.get_organization_id())
		set_organization_activity(self.get_user_id(), self.get_organization_id(), self.object)
		self.clear_messages()
		return super(OrganizationActivityCreateView, self).form_valid(form)		



# Khung nhìn chung quản lý danh sách thành viên
class BaseOrganizationMemberView(BaseOrganizationView):

	can_set = 0

	def get_context_data(self, **kwargs):
		if not is_organization_manager(self.get_user_id(), self.get_organization_id()):
			raise PermissionDenied

		context = super(BaseOrganizationMemberView, self).get_context_data(**kwargs)

		context['members_active'] ='active'

		if is_organization_administrator(self.get_user_id(), self.get_organization_id()):
			self.can_set = 1
			context['can_set'] = 'active'

		return context



# Khung nhìn xem danh sách thành viên trong tổ chức
class OrganizationMemberListView(BaseOrganizationMemberView, ListView):
	template_name = 'v1/organization/profile/member/list.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(OrganizationMemberListView, self).get_context_data(**kwargs)
		
		context['theads'] = [	{'name': u'#', 'size' : '10%'},
								{'name': u'Họ và Tên', 'size' : 'auto'},	]

		if self.can_set:
			context['show_add_button'] = 1
			context['show_import_button'] = 1
			context['show_checkbox'] = 1
			context['show_statistics_button'] = 1
			context['import_link'] = 'import/'

		return context

	def get_queryset(self):
		user_list = get_organization_user_list(self.get_user_id(), self.get_organization_id())
		objects = []
		can_set = is_organization_administrator(self.get_user_id(), self.get_organization_id())
		for obj in user_list:
			values = []
			if can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="%s" name="list"/>' % obj.identify))
			values.append(obj.identify)
			values.append(mark_safe(u'<a href="/user/user=%s">%s</a>' % (obj.identify, obj.get_full_name())))

			# Thêm cột các tổ chức tham gia


			objects.append(values)
		return objects



# Khung nhìn nhập danh sách thành viên vào tổ chức
class OrganizationMemberImportView(BaseOrganizationMemberView, BaseImportView):
	template_name = 'v1/organization/profile/member/import.html'

	CONST_FIELDS = ['identify']

	def get_success_url(self):
		return reverse('organization_member_list_view_v1', kwargs={ 'organization_id' : self.get_organization_id() })

	def get_context_data(self, **kwargs):
		if not is_organization_administrator(self.get_user_id(), self.get_organization_id()):
			raise PermissionDenied

		context = super(OrganizationMemberImportView, self).get_context_data(**kwargs)
		
		return context

	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		identify = row['identify']
		if set_organization_user(self.get_user_id(), self.get_organization_id(), identify):
			print 'Import member ' + identify + ' to ' + self.get_organization_id() + ' complete'
			print '----------'
			return True

		return False



# Khung nhìn xem các tổ chức trực thuộc
class ChildOrganizationTreeView(BaseOrganizationView, TemplateView):
	template_name = 'v1/organization/profile/child_organization.html'

	def get_context_data(self, **kwargs):
		context = super(ChildOrganizationTreeView, self).get_context_data(**kwargs)
		
		context['organization_tree_active'] = 'active'
		context['tree_content'] = mark_safe(self.toHtml(get_organization_tuple_table(self.get_organization_id())))

		if is_organization_administrator(self.get_user_id(), self.get_organization_id()):
			context['can_set_list'] = 1
			
		return context

	def toHtml(self, table):
		html = ''
		if len(table[1]) > 0:
			html += '<ul>'
			for obj in table[1]:
				html += '<li><a href="/organization/organization=%s/">' % obj[0].identify
				html += obj[0].name
				html += '</a>'
				html += self.toHtml(obj)
				html += '</li>'
			html += '</ul>'
		return html



class OrganizationFormView(BaseSuccessMessageMixin, FormView, BaseView):
	def get_form(self, form_class):
		form = super(OrganizationFormView, self).get_form(form_class)
		form.fields['name'].widget.attrs['class'] = 'form-control'
		form.fields['short_name'].widget.attrs['class'] = 'form-control'
		form.fields['organization_type'].widget.attrs['class'] = 'form-control'
		form.fields['management_organization'].widget.attrs['class'] = 'form-control'
		form.fields['description'].widget.attrs['class'] = 'form-control'
		return form



class OrganizationCreateView(CreateView, OrganizationFormView):
	model = get_organization_model()

	template_name = 'v1/organization/editor/creator.html'

	success_message = u'Thêm tổ chức thành công'

	fields =['identify', 'name', 'short_name', 'organization_type', 'management_organization', 'description']

	def get_success_url(self):
		return reverse('organization_list_view_v1')

	def get_form(self, form_class):
		form = super(OrganizationCreateView, self).get_form(form_class)
		form.fields['identify'].widget.attrs['class'] = 'form-control'
		return form

	def get_context_data(self, **kwargs):
		if not is_organization_administrator(self.request.session['user_id']):
			raise PermissionDenied

		context = super(OrganizationCreateView, self).get_context_data(**kwargs)
		
		context['title'] = u'Thêm tổ chức'

		context['page_title'] = u'Thêm tổ chức'

		context['organization_active'] = 'active'
		
		context['button_value'] = u'Thêm'

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		set_organization(self.get_user_id(), self.object)
		self.clear_messages()
		return super(OrganizationCreateView, self).form_valid(form)



class BaseOrganizationUpdateView(BaseOrganizationView):
	def get_context_data(self, **kwargs):
		if not is_organization_administrator(self.get_user_id(), self.get_organization_id()):
			raise PermissionDenied

		context = super(BaseOrganizationUpdateView, self).get_context_data(**kwargs)

		return context



class OrganizationUpdateView(BaseOrganizationUpdateView, OrganizationFormView, UpdateView):
	template_name = 'v1/organization/editor/update.html'

	fields =['name', 'short_name', 'organization_type', 'management_organization', 'description']

	success_message = u'Cập nhật thành công'

	def get_context_data(self, **kwargs):
		context = super(OrganizationUpdateView, self).get_context_data(**kwargs)

		return context

	def get_success_url(self):
		return reverse('organization_update_view_v1', kwargs={'organization_id' : self.get_organization_id() })

	def get_context_data(self, **kwargs):
		context = super(OrganizationUpdateView, self).get_context_data(**kwargs)

		context['button_value'] = u'Cập nhật'

		return context

	def form_valid(self,form):
		self.object = form.save(commit=False)
		set_organization(self.get_user_id(), self.object)
		self.clear_messages()
		return super(OrganizationUpdateView, self).form_valid(form)

	def get_object(self):
		return get_organization(self.get_organization_id())



class OrganizationPermissionListView(BaseOrganizationUpdateView, ListView):
	template_name = 'v1/organization/editor/permission/list.html'

	def get_context_data(self, **kwargs):
		context = super(OrganizationPermissionListView, self).get_context_data(**kwargs)

		context['theads'] = [	{'name': u'Họ và tên', 'size' : 'auto'},
								{'name': u'Chức vụ', 'size' : '15%'},
								{'name': u'Quyền hạn', 'size' : '15%'},	]

		context['show_add_button'] = 1
		context['show_import_button'] = 1
		context['add_link'] = 'create/'
		context['import_link'] = 'import/'

		return context

	def get_queryset(self):
		organization_staff_list = get_organization_staff(self.get_organization_id())

		objects = []
		for obj in organization_staff_list:
			values = []
			values.append(obj.user.get_full_name())
			values.append(obj.position.name)
			values.append(obj.permission)
			objects.append(values)

		return objects



class OrganizationPermissionCreateView(BaseOrganizationUpdateView, BaseSuccessMessageMixin, CreateView):
	template_name = 'v1/organization/editor/permission/creator.html'

	# form_class = OrganizationPermissionForm
	model = get_organization_user_model()

	success_message = u'Thêm quyền hạn thành công'

	fields =['user', 'permission', 'position']

	def get_success_url(self):
		return reverse('organization_permission_list_view_v1',  kwargs={ 'organization_id' : self.get_organization_id() })

	def get_form(self, form_class):
		form = super(OrganizationPermissionCreateView, self).get_form(form_class)
		
		# form.fields['identify'].widget.attrs['class'] = 'form-control'

		return form

	def get_context_data(self, **kwargs):
		if not is_organization_administrator(self.request.session['user_id']):
			raise PermissionDenied

		context = super(OrganizationPermissionCreateView, self).get_context_data(**kwargs)
		
		context['title'] = u'Thêm quyền hạn người dùng trong tổ chức'

		context['page_title'] = u'Thêm quyền hạn người dùng trong tổ chức'

		context['organization_active'] = 'active'
		
		context['button_value'] = u'Thêm'

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.organization = get_organization(self.get_organization_id())
		set_organization_user(self.get_user_id(), self.object)
		self.clear_messages()
		return super(OrganizationPermissionCreateView, self).form_valid(form)





class OrganizationPermissionUpdateView(BaseOrganizationUpdateView, BaseSuccessMessageMixin, UpdateView):
	template_name = 'v1/organization/editor/permission/creator.html'

	# form_class = OrganizationPermissionForm
	model = get_organization_user_model()

	success_message = u'Thêm quyền hạn thành công'

	fields =['user', 'permission', 'position']

	def get_success_url(self):
		return reverse('organization_permission_list_view_v1',  kwargs={ 'organization_id' : self.get_organization_id() })

	def get_form(self, form_class):
		form = super(OrganizationPermissionCreateView, self).get_form(form_class)
		
		# form.fields['identify'].widget.attrs['class'] = 'form-control'

		return form

	def get_context_data(self, **kwargs):
		if not is_organization_administrator(self.request.session['user_id']):
			raise PermissionDenied

		context = super(OrganizationPermissionCreateView, self).get_context_data(**kwargs)
		
		context['title'] = u'Chỉnh sửa quyền hạn người dùng trong tổ chức'

		context['page_title'] = u'Chỉnh sửa quyền hạn người dùng trong tổ chức'

		context['organization_active'] = 'active'
		
		context['button_value'] = u'Chỉnh sửa'

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.organization = get_organization(self.get_organization_id())
		set_organization_user(self.get_user_id(), self.object)
		self.clear_messages()
		return super(OrganizationPermissionCreateView, self).form_valid(form)





class OrganizationListView(BaseView, ListView):
	template_name = 'v1/static_pages/list.html'
	paginate_by = '20'

	can_set = False

	def get_context_data(self, **kwargs):
		context = super(OrganizationListView, self).get_context_data(**kwargs)
		
		context['title'] = u'Danh sách tổ chức'
		context['page_title'] = u'Danh sách tổ chức'

		context['organization_active'] = 'active'
		context['organization_list_active'] = 'active'

		context['theads'] = [	{'name': u'#', 'size' : '10%'},
								{'name': u'Tên tổ chức', 'size' : 'auto'},
								{'name': u'Loại tổ chức', 'size' : '15%'},	]


		if self.can_set:
			context['show_add_button'] = 1
			context['show_import_button'] = 1
			context['add_link'] = '/organization/create/'
			context['import_link'] = '/organization/import/'

		#  context['can_set_list'] = 1

		return context

	def get_queryset(self):
		user_id = self.request.session['user_id']

		organization_list = None

		self.can_set = is_super_administrator(self.get_user_id())

		if is_super_administrator(self.get_user_id()):
			organization_list = get_organization_list()
		else:
			organization_list = get_joined_organization_list(self.get_user_id())

		objects = []
		if organization_list is not None:
			for obj in organization_list:
				values = []
				# if self.can_set:
				# 	values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.identify))
				values.append(obj.identify)
				values.append(mark_safe(u'<a href="/organization/organization=%s"">%s</a>' % (obj.identify, obj.name)))
				values.append(obj.organization_type.name)
				objects.append(values)

		return objects



class OrganizationTreeView(BaseView, TemplateView):
	template_name = 'v1/organization/organization_tree_list.html'

	def get_context_data(self, **kwargs):
		context = super(OrganizationTreeView, self).get_context_data(**kwargs)
		
		org = get_organization_root()

		context['organization_active'] = 'active'
		context['organization_tree_active'] = 'active'

		context['page_title'] = u'Cây tổ chức'

		context['tree_content'] = mark_safe(self.toHtml(get_organization_tuple_table()))

		context['can_manage_organization'] = 1

		return context

	def toHtml(self, table):
		html = ''
		if len(table[1]) > 0:
			html += '<ul>'
			for obj in table[1]:
				html += '<li><a href="/organization/organization=%s/">' % obj[0].identify
				html += obj[0].name
				html += '</a>'
				html += self.toHtml(obj)
				html += '</li>'
			html += '</ul>'
		return html



class OrganizationImportView(BaseView, BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = (	'identify',
						'name',
						'organization_type',
						'management_organization'	)

	def get_success_url(self):
		return reverse('organization_list_view_v1')

	def get_context_data(self, **kwargs):
		if not is_organization_administrator(self.get_user_id()):
			raise PermissionDenied
		context = super(OrganizationImportView, self).get_context_data(**kwargs)
		
		context['page_title'] = u'Nhập danh sách tổ chức'

		return context

	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		identify = row['identify']
		name = row['name']
		organization_type = row['organization_type']
		management_organization = row['management_organization']

		if management_organization is not None and len(management_organization) == 0:
			management_organization = None

		if set_organization(self.get_user_id(), identify, name, organization_type, management_organization):
			print 'Import organization ' + identify + ' successfully'
			print '----------'
			return True

		return False