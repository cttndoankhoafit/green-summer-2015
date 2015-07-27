# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.utils.html import mark_safe

from mms_backoffice.models import *
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView

from django.http import HttpResponseRedirect, HttpResponse, Http404

from django.core.urlresolvers import reverse_lazy, reverse

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_controller.resources_temp import *

from mms_webapp_v1.forms.organization import *

from mms_webapp_v1.views.bases.base_view import *



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
class OrganizationDetailView(BaseOrganizationView, DetailView):
	template_name = 'v1/organization/organization_overview.html'

	def get_context_data(self, **kwargs):
		context = super(OrganizationDetailView, self).get_context_data(**kwargs)
		context['overview_active'] ='active'

		return context

	def get_object(self):
		return get_organization(self.get_organization_id())



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
	template_name = 'v1/organization/activity/list.html'
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

		return context

	def get_queryset(self):
		activity_list = get_organization_activity_list(self.get_user_id(), self.get_organization_id())

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
	template_name = 'v1/organization/activity/import.html'

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

	template_name = 'v1/organization/activity/create.html'

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




# Khung nhìn chung quản lý danh sách hoạt động của tổ chức
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
	template_name = 'v1/organization/member/list.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(OrganizationMemberListView, self).get_context_data(**kwargs)
		
		context['theads'] = [	{'name': u'#', 'size' : '10%'},
								{'name': u'Họ và Tên', 'size' : 'auto'},	]

		if self.can_set:
			context['show_add_button'] = 1
			context['show_delete_button'] = 1
			context['show_checkbox'] = 1

		return context

	def get_queryset(self):
		user_list = get_all_user_in_user_managed_organization(self.get_user_id(), self.get_organization_id())
		objects = []
		can_set = is_organization_administrator(self.get_user_id(), self.get_organization_id())
		for obj in user_list:
			values = []
			if can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="%s" name="list"/>' % obj.identify))
			values.append(obj.identify)
			values.append(mark_safe(u'<a href="/user/user=%s">%s</a>' % (obj.identify, obj.get_full_name())))
			objects.append(values)
		return objects



# Khung nhìn nhập danh sách thành viên vào tổ chức
class OrganizationMemberImportView(BaseOrganizationMemberView, BaseImportView):
	template_name = 'v1/organization/member/import.html'

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
		if add_organization_user(self.get_user_id(), self.get_organization_id(), identify):
			print 'Import member ' + identify + ' to ' + self.get_organization_id() + ' complete'
			print '----------'
			return True

		return False



# Khung nhìn xem các tổ chức trực thuộc
class ChildOrganizationTreeView(BaseOrganizationView, TemplateView):
	template_name = 'v1/organization/organization_child_organization.html'

	def get_context_data(self, **kwargs):
		context = super(ChildOrganizationTreeView, self).get_context_data(**kwargs)
		
		context['organization_tree_active'] = 'active'
		context['tree_content'] = mark_safe(self.toHtml(get_organization_tuple_table(self.get_user_id(), self.get_organization_id())))

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



		




class OrganizationFormView(BaseSuccessMessageMixin, FormView):
	def get_form(self, form_class):
		form = super(OrganizationFormView, self).get_form(form_class)
		form.fields['identify'].widget.attrs['class'] = 'form-control'
		form.fields['name'].widget.attrs['class'] = 'form-control'
		form.fields['organization_type'].widget.attrs['class'] = 'form-control'
		form.fields['manager_organization'].widget.attrs['class'] = 'form-control'

		return form

class OrganizationCreateView(CreateView, OrganizationFormView):
	model = get_organization_model()

	form_class = OrganizationForm

	template_name = 'v1/organization/organization_editor.html'# template of OrganizationCreateView is the same as UserCreateView

	success_message = u'Thêm tổ chức thành công'

	def get_form(self, form_class):
		kwargs = self.get_form_kwargs()

		params = {}
		params['user_id'] = self.request.session['user_id']

		return form_class(params, **kwargs)

	def get_success_url(self):
		return reverse('organization_list_view_v1')

	def get_context_data(self, **kwargs):
		if not is_organization_administrator(self.request.session['user_id']):
			raise PermissionDenied

		context = super(OrganizationCreateView, self).get_context_data(**kwargs)
		
		context['title'] = u'Thêm tổ chức'

		context['page_title'] = u'Thêm tổ chức'

		context['organization_active'] = 'active'
		
		context['button_name'] = u'Thêm tổ chức'

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		set_organization(self.request.session['user_id'], self.object)
		self.clear_messages()
		return super(OrganizationCreateView, self).form_valid(form)

class OrganizationListView(ListView):
	template_name = 'v1/list.html'
	paginate_by = '20'

	can_set = False

	def get_context_data(self, **kwargs):
		context = super(OrganizationListView, self).get_context_data(**kwargs)
		
		context['title'] = u'Danh sách tổ chức'
		context['page_title'] = u'Danh sách tổ chức'

		context['organization_active'] = 'active'
		context['organization_list_active'] = 'active'

		context['theads'] = [	{'name': u'Tên tổ chức', 'size' : 'auto'},
								# {'name': u'Trạng thái', 'size' : '20%'},
								{'name': '', 'size' : '8%'},	]

		context['add_link'] = '/organization/create/'
		context['import_link'] = '/organization/import/'

		#  context['can_set_list'] = 1

		return context

	def get_queryset(self):
		user_id = self.request.session['user_id']
		# if not can_user_manage_organization(user_id):
		# 	raise PermissionDenied

		organization_list = None

		# self.can_set = can_user_administrate_organization(user_id)

		if is_super_administrator_id(user_id):
			organization_list = get_organization_list(user_id)
		else:
			organization_list = get_paticipate_organizations(user_id)
		
		objects = []
		if organization_list is not None:
			for obj in organization_list:
				values = []
				if self.can_set:
					values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.identify))
				values.append(obj.name)
				values.append(mark_safe(u'<a href="/organization/organization=%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.identify)))
				objects.append(values)

		return objects



class OrganizationTreeView(TemplateView):
	template_name = 'v1/organization/organization_tree_all.html'

	def get_context_data(self, **kwargs):
		if not is_super_administrator_id(self.request.session['user_id']):
			raise PermissionDenied

		context = super(OrganizationTreeView, self).get_context_data(**kwargs)
		
		org = get_organization_root()

		context['organization_active'] = 'active'
		context['organization_tree_active'] = 'active'

		context['tree_content'] = mark_safe(self.toHtml(get_organization_tuple_table(self.request.session['user_id'], get_organization_root()))
		)

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



class OrganizationImportView(BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = (	'identify',
						'name',
						'organization_type',
						'manager_organization'	)

	def get_success_url(self):
		return reverse('organization_tree_view_v1')

	def get_context_data(self, **kwargs):
		context = super(OrganizationImportView, self).get_context_data(**kwargs)
		if not is_organization_administrator(self.request.session['user_id']):
			raise PermissionDenied

		return context

	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		identify = row['identify']
		name = row['name']
		organization_type = row['organization_type']
		manager_organization = row['manager_organization']

		if manager_organization is not None and len(manager_organization) == 0:
			manager_organization = None

		if set_organization(self.request.session['user_id'], identify, name, organization_type, manager_organization):
			print 'Import organization ' + identify + ' successfully'
			print '----------'
			return True

		return False


class OrganizationManagementImportView(BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = (	'manager_organization',
						'managed_organization'	)

	def get_success_url(self):
		return reverse('organization_tree_view_v1')

	def get_context_data(self, **kwargs):
		context = super(OrganizationManagementImportView, self).get_context_data(**kwargs)
		if not is_organization_administrator(self.request.session['user_id']):
			raise PermissionDenied

		return context

	def input_row(self, row):
		try:
			for field in self.CONST_FIELDS:
				print row[field]
		except Exception as e:
			return e
		
		manager_organization = row['manager_organization']
		managed_organization = row['managed_organization']
		
		create_organization_managerment_by_infomation(	self.request.session['user_id'],
														manager_organization,
														managed_organization	)

		print '-------------'
		return 'ok'






class BaseOrganizationUpdateView(UpdateView, OrganizationFormView):
	model = get_organization_model
	fields = '__all__'
	success_message = u'Cập nhật thành công'

	def get_context_data(self, **kwargs):
		context = super(BaseOrganizationUpdateView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin tổ chức'
		context['page_title'] = u'Thông tin tổ chức'
		
		context['organization_active'] = 'active'

		context['member_full_name'] = self.object.get_full_name()

		return context



class OrganizationUpdateView(BaseOrganizationUpdateView):
	template_name = 'v1/user/user_update.html'
	template_name = 'v1/user/user_update.html'

	def get_success_url(self):
		return reverse('organization_update_view_v1', kwargs={'organization_id' : self.kwargs['organization_id'] })

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.creator = self.request.user
		self.object.status = 0

		organization__id = self.request.session['organization__id']
		user = self.kwargs['organization__id']

		# if int(user) == user_id:
		# 	self.request.session['user_full_name'] = self.object.get_full_name()
		
		self.object.save()

		self.clear_messages()

		return super(OrganizationUpdateView, self).form_valid(form)

	def get_object(self):
		try:
			return set_user(	self.request.session['organization__id'],
							self.kwargs['organization__id']
						)

		except:
			raise Http404('Organization does not exist!')

#########################################
# class BaseOrganizationUpdateView(UpdateView, OrganizationFormView):
# 	model = get_organization_model
# 	fields = '__all__'
# 	success_message = u'Cập nhật thành công'

# 	def get_context_data(self, **kwargs):
# 		context = super(BaseOrganizationUpdateView, self).get_context_data(**kwargs)

# 		context['title'] = u'Thông tin tổ chức'
# 		context['page_title'] = u'Thông tin tổ chức'
		
# 		context['organization_active'] = 'active'

# 		context['member_full_name'] = self.object.get_full_name()

# 		return context
# class OrganizationUpdateView(BaseOrganizationUpdateView):
# 	template_name = 'v1/user/user_update.html'
# 	template_name = 'v1/user/user_update.html'

# 	def get_success_url(self):
# 		return reverse('organization_update_view_v1', kwargs={'organization_id' : self.kwargs['organization_id'] })

# 	def form_valid(self,form):
# 		self.object = form.save(commit=False)
# 		self.object.creator = self.request.user
# 		self.object.status = 0

# 		organization__id = self.request.session['organization__id']
# 		user = self.kwargs['organization__id']

# 		# if int(user) == user_id:
# 		# 	self.request.session['user_full_name'] = self.object.get_full_name()
		
# 		self.object.save()

# 		self.clear_messages()

# 		return super(OrganizationUpdateView, self).form_valid(form)

# 	def get_object(self):
# 		try:
# 			return set_user(	self.request.session['organization__id'],
# 							self.kwargs['organization__id']
# 						)

# 		except:
# 			raise Http404(error_organization_not_exist_message)




