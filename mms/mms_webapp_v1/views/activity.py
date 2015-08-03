# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.utils.html import mark_safe
from django.core.urlresolvers import reverse
from django.views.generic import ListView, UpdateView, TemplateView, DetailView, CreateView, View, FormView
from django.http import HttpResponseRedirect, Http404

from mms_backoffice.models import Activity, ActivityUser

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_base.resources import *

from mms_webapp_v1.views.bases.base_view import *

#from mms_webapp_v1.forms.activity import ActivityForm


class BaseActivityView(BaseView):

	def get_activity_id(self):
		return self.kwargs['activity_id']
	
	def get_context_data(self, **kwargs):
		context = super(BaseActivityView, self).get_context_data(**kwargs)

		context['activity_id'] = self.get_activity_id()

		context['page_title'] = get_activity(self.get_activity_id()).name
		
		context['activity_full_name'] = context['page_title']
		
		context['activity_active'] = 'active'

		if is_activity_administrator(self.get_user_id(), self.get_activity_id()):
			context['activity_administrator'] = 1

		if is_activity_manager(self.get_user_id(), self.get_activity_id()):
			context['activity_manager'] = 1

		return context
		


class ActivityListView(BaseView, ListView, FormView):
	template_name = 'v1/activity/explorer.html'
	paginate_by = '20'

	# can_set = True

	organization_id = ''

	def get_context_data(self, **kwargs):
		context = super(ActivityListView, self).get_context_data(**kwargs)

		context['title'] = u'Danh sách hoạt động'
		context['page_title'] = u'Danh sách hoạt động'

		context['activity_active'] = 'active'
		context['activity_list_active'] = 'active'

		context['theads'] = [	{'name': u'Tên hoạt động', 'size' : 'auto'},
								{'name': u'Thời gian', 'size' : '15%'},	]
		context['add_link'] = '/activity/create/'

		# if self.can_set:
		# 	context['show_add_button'] = 1
		# 	context['show_delete_button'] = 1
		# 	context['show_import_button'] = 1
		# 	context['show_checkbox'] = 1
		# 	context['can_set_list'] = 1

		if 'organization_id' in self.kwargs:
			self.organization_id = self.kwargs['organization_id']

		context['tree_content'] = mark_safe(self.toHtml(get_organization_tuple_table()))

		return context

	def get_color(self, value):
		if value == 0:
			return 'blue'
		elif value == 1:
			return 'green'
		elif value == 2:
			return 'purple'

	def get_queryset(self):
		activity_list = None

		if 'organization_id' in self.kwargs:
			activity_list = get_organization_activity_list(self.kwargs['organization_id'])
		else:
			activity_list = get_activity_list()

		objects = []
		for obj in activity_list:
			values = []
			# if self.can_set:
			# 	values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.identify))
			activity_link = u'<a href="/activity/activity=%s"">%s </a>' % (obj.identify, obj.name)

			if can_register_activity(self.get_user_id(), obj.identify):
				activity_link += u'<span class="label label-sm label-danger ">Đăng ký <i class="fa fa-bell-o"></i></span>'
			elif is_participated_activity(self.get_user_id(), obj.identify):
				activity_link += u'<span class="label label-sm label-success">Đã tham gia</span>'

			values.append(mark_safe(activity_link))

			values.append(obj.start_time)
			objects.append(values)
		return objects

	def toHtml(self, table):
		html = ''
		if len(table[1]) > 0:
			html += '<ul>'
			for obj in table[1]:
				if obj[0].identify == self.organization_id:
					html += '<li><a href="/activity/list/organization=%s/" title="%s" class="jstree-clicked">' % (obj[0].identify, obj[0].name)
				else:
					html += '<li><a href="/activity/list/organization=%s/" title="%s">' % (obj[0].identify, obj[0].name)
				html += unicode(obj[0].short_name)
				html += '</a>'
				html += self.toHtml(obj)
				html += '</li>'
			html += '</ul>'
		return html


	
	def post(self, request, *args, **kwargs):
		print request.POST
		if 'register' in request.POST:
			todel = request.POST.getlist('register')
			print todel
		return self.get(self, *args, **kwargs) #HttpResponseRedirect(reverse('user_list_view_v1'))



class ActivityDetailView(BaseActivityView, DetailView):
	template_name = 'v1/activity/profile/overview.html'

	activity_object = None

	def get_context_data(self, **kwargs):
		context = super(ActivityDetailView, self).get_context_data(**kwargs)
		activity_object = get_activity(self.kwargs['activity_id'])
		
		context['activity_type'] = activity_object.activity_type.name
		context['management_organization'] = mark_safe(u'<a href="/organization/organization=%s">%s</a>' % (activity_object.organization.identify, activity_object.organization.name))

		context['staff_list'] = self.get_staff()

		if can_register_activity(self.get_user_id(), self.get_activity_id()):
			context['state'] = mark_safe(u'<input type="submit" class="btn blue" value="Đăng ký">')
		else:
			activity_user_object = get_activity_user(self.get_user_id(), self.get_activity_id())
			if activity_user_object is None:
				context['state'] = u'Bạn không thể đăng ký hoạt động này'
			elif activity_user_object.participated:
				context['state'] = u'Bạn đã tham gia hoạt động này'
			else:
				context['state'] = u'Bạn đã đăng ký hoạt động này'
		return context

	def get_staff(self):
		activity_staff_list = get_activity_staff(self.get_activity_id())

		objects = []
		for obj in activity_staff_list:
			objects.append({ 'name' : obj.user.get_full_name(), 'position' : obj.position })

		return objects

	def get_object(self):
		return get_activity(self.get_activity_id())


class ActivityMemberListView(BaseActivityView, ListView):
	template_name = 'v1/activity/profile/list.html'
	paginate_by = '20'

	can_set = False

	def get_context_data(self, **kwargs):
		if not is_activity_manager(self.get_user_id(), self.get_activity_id()):
			raise PermissionDenied

		context = super(ActivityMemberListView, self).get_context_data(**kwargs)

		context['theads'] = [	{'name': u'#', 'size' : '10%'},
								{'name': u'Tên sinh viên', 'size' : 'auto'},
								{'name': u'Ghi chú', 'size' : '20%'},	]

		if self.can_set:
			context['show_add_button'] = 1
			context['show_delete_button'] = 1
			context['show_import_button'] = 1
			context['show_checkbox'] = 1
			context['show_statistics_button'] = 1
			context['import_link'] = 'import/'

		return context

	def get_queryset(self):
		activity_user_list = get_activity_user_list(self.get_user_id(), self.get_activity_id())

		self.can_set = is_activity_administrator(self.get_user_id(), self.get_activity_id())

		objects = []
		for obj in activity_user_list:
			values = []
			if self.can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.user.identify))
			values.append(obj.user.identify)
			values.append(obj.user.get_full_name())	
			values.append(obj.note)	
			objects.append(values)
		return objects


# Khung nhìn chuẩn cho các khung nhìn có dạng mẫu (Form)
class ActivityFormView(BaseSuccessMessageMixin, FormView):
	def get_form(self, form_class):
		form = super(ActivityFormView, self).get_form(form_class)
		
		# form.fields['identify'].widget.attrs['class'] = 'form-control'
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

		form.fields['description'].widget.attrs['class'] = 'form-control'
		form.fields['location'].widget.attrs['class'] = 'form-control'
		
		return form



class BaseActivityUpdateView(BaseActivityView):
	def get_context_data(self, **kwargs):
		if not is_activity_administrator(self.get_user_id(), self.get_activity_id()):
			raise PermissionDenied

		context = super(BaseActivityUpdateView, self).get_context_data(**kwargs)

		return context



class ActivityUpdateView(BaseActivityUpdateView, ActivityFormView, UpdateView):
	template_name = 'v1/activity/editor/update.html'

	success_message = u'Cập nhật thông tin thành công'

	fields =[	'name',
				'activity_type',
				'start_time',
				'end_time',
				'location',
				'register_start_time',
				'register_end_time',
				'published',
				'credits',
				'score',
				'description',	]

	def get_success_url(self):
		return reverse('activity_update_view_v1', kwargs={ 'activity_id' : self.get_activity_id() })

	def form_valid(self,form):
		self.object = form.save(commit=False)
		set_activity(self.get_user_id(), self.object)

		self.clear_messages()

		return super(ActivityUpdateView, self).form_valid(form)

	def get_object(self):
		return get_activity(self.get_activity_id())


# Khung nhìn tạo một hoạt động
# class ActivityCreateView(CreateView, ActivityFormView):
# 	model = Activity

# #	form_class = ActivityForm

# 	template_name = 'v1/activity/activity_create.html'

# 	success_message = u'Thêm hoạt động thành công'

# 	def get_success_url(self):
# 		return reverse('activity_list_view_v1')

# 	def get_form(self, form_class):
# 		kwargs = self.get_form_kwargs()

# 		params = {}
# 		params['user_id'] = self.request.session['user_id']
		
# 		return form_class(params, **kwargs)


# 	def form_valid(self, form):
# 		self.object = form.save(commit=False)
# 		return super(ActivityCreateView, self).form_valid(form)



class ActivityMemberImportView(BaseActivityView, BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = ['user', 'participated']
	
	def get_success_url(self):
		return reverse('activity_member_list_view_v1', kwargs = { 'activity_id' : self.get_activity_id() } )

	def input_row(self, row):

		if not self.check_input_row_valid(row):
			return False
		
		user = row['user']
		participated = bool(row['participated'])

		if set_activity_user(user, self.get_activity_id(), 2, None, participated):
			print 'Import user ' + user + ' to ' + self.get_activity_id() + ' complete'
			print '----------'
			return True

		return False


class ActivityPermissionListView(BaseActivityUpdateView, ListView):
	template_name = 'v1/activity/editor/permission/list.html'

	def get_context_data(self, **kwargs):
		context = super(ActivityPermissionListView, self).get_context_data(**kwargs)

		context['theads'] = [	{'name': u'Họ và tên', 'size' : 'auto'},
								{'name': u'Chức vụ', 'size' : '15%'},
								{'name': u'Quyền hạn', 'size' : '15%'},	]

		context['show_add_button'] = 1
		context['show_import_button'] = 1
		context['add_link'] = 'create/'
		context['import_link'] = 'import/'

		return context

	def get_queryset(self):
		activity_staff_list = get_activity_staff(self.get_activity_id())

		objects = []
		for obj in activity_staff_list:
			values = []
			values.append(mark_safe('<a href="/activity/activity=%s/permission/user=%s/">%s</a>' % (self.get_activity_id(), obj.user.identify, obj.user.get_full_name())))
			values.append(obj.position)
			values.append(obj.get_permission_display())
			objects.append(values)

		return objects

class BaseActivityPermissionView(BaseActivityUpdateView, BaseSuccessMessageMixin, FormView):

	def get_context_data(self, **kwargs):
		context = super(BaseActivityPermissionView, self).get_context_data(**kwargs)

		return context

	def get_form(self, form_class):
		form = super(BaseActivityPermissionView, self).get_form(form_class)
		
		form.fields['permission'].widget.attrs['class'] = 'form-control'
		form.fields['position'].widget.attrs['class'] = 'form-control'

		return form
		


class ActivityPermissionCreateView(BaseActivityPermissionView, CreateView):
	template_name = 'v1/activity/editor/permission/creator.html'

	# form_class = OrganizationPermissionForm
	model = get_activity_user_model()

	success_message = u'Thêm quyền hạn thành công'

	fields =['user', 'permission', 'position']

	def get_success_url(self):
		return reverse('activity_permission_list_view_v1',  kwargs={ 'activity_id' : self.get_activity_id() })

	def get_form(self, form_class):
		form = super(ActivityPermissionCreateView, self).get_form(form_class)
		
		form.fields['user'].widget.attrs['class'] = 'form-control'
	
		return form

	def get_context_data(self, **kwargs):
		context = super(ActivityPermissionCreateView, self).get_context_data(**kwargs)
	
		context['button_value'] = u'Thêm'

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.activity = get_activity(self.get_activity_id())
		set_activity_user(self.get_user_id(), self.object)
		self.clear_messages()
		return super(ActivityPermissionCreateView, self).form_valid(form)



class ActivityPermissionUpdateView(BaseActivityPermissionView, UpdateView):

	template_name = 'v1/activity/editor/permission/update.html'

	success_message = u'Chỉnh sửa quyền hạn thành công'

	fields =['permission', 'position']

	def get_success_url(self):
		return reverse('activity_permission_update_view_v1',  kwargs={ 'activity_id' : self.get_activity_id(), 'user_id' : self.kwargs['user_id'] })

	def get_context_data(self, **kwargs):
		context = super(ActivityPermissionUpdateView, self).get_context_data(**kwargs)
		
		context['button_value'] = u'Chỉnh sửa'

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		set_activity_user(self.get_user_id(), self.object)
		self.clear_messages()
		return super(ActivityPermissionUpdateView, self).form_valid(form)

	def get_object(self):
		return get_activity_user(self.kwargs['user_id'], self.get_activity_id())



class ActivityPermissionImportView(BaseActivityUpdateView, BaseImportView):

	template_name = 'v1/activity/editor/permission/import.html'

	success_message = u'Nhập thông tin quyền hạn thành công'

	CONST_FIELDS = ['user', 'permission', 'position']

	def get_success_url(self):
		return reverse('activity_permission_list_view_v1',  kwargs={ 'activity_id' : self.get_activity_id() })


	def get_context_data(self, **kwargs):
		context = super(ActivityPermissionImportView, self).get_context_data(**kwargs)
		
		return context

	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		user = row['user']
		permission = int(row['permission'])
		position = row['position']

		if set_activity_user(user, self.get_activity_id(), permission, position):
			print 'Import staff ' + user + ' to ' + self.get_activity_id() + ' complete'
			print '----------'
			return True

		return False