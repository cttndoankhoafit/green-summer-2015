# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.utils.html import mark_safe
from django.core.urlresolvers import reverse
from django.views.generic import ListView, UpdateView, TemplateView, DetailView, CreateView, View
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
								{'name': u'Thời gian', 'size' : '15%'},
								{'name': u'', 'size' : '15%'},
							]
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
			values.append(mark_safe(u'<a href="/activity/activity=%s"">%s</a>' % (obj.identify, obj.name)))
			values.append(obj.start_time)
			if can_register_activity(self.get_user_id(), obj.identify):
				values.append(mark_safe(u'<input type="submit" class="btn default btn-xs green-stripe" name="register" values="%s" title="%s">' % (obj.identify, u'Đăng ký')))
			else:
				values.append('')
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
	template_name = 'v1/activity/activity_overview.html'

	def get_object(self):
		return get_activity(self.kwargs['activity_id'])


class ActivityMemberListView(BaseActivityView, ListView):
	template_name = 'v1/activity/activity_member.html'
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


class ActivityImportView(BaseImportView):
	template_name = 'v1/import.html'

	# CONST_FIELDS = (	'identify',
	# 					'name',
	# 					'organization_type'	)

	# def get_success_url(self):
	# 	return reverse('organization_tree_view_v1')

	# def input_row(self, row):
	# 	try:
	# 		for field in self.CONST_FIELDS:
	# 			print row[field]
	# 	except Exception as e:
	# 		return e
		
	# 	identify = row['identify']
	# 	name = row['name']
	# 	organization_type = row['organization_type']

	# 	create_organization_by_infomation(	self.request.session['user_id'],
	# 										identify,
	# 										name,
	# 										organization_type	)

	# 	print '-------------'
	# 	return 'ok'



# Khung nhìn chuẩn cho các khung nhìn có dạng mẫu (Form)
class BaseActivityFormView(BaseSuccessMessageMixin, FormView):
	def get_form(self, form_class):
		form = super(BaseActivityFormView, self).get_form(form_class)

		form.fields['identify'].widget.attrs['class'] = 'form-control'
		form.fields['name'].widget.attrs['class'] = 'form-control'
		form.fields['activity_type'].widget.attrs['class'] = 'form-control'

		form.fields['organization'].widget.attrs['class'] = 'form-control'
		
		form.fields['start_time'].widget.attrs['class'] = 'form-control'

		form.fields['start_time'].widget.attrs['class'] = 'form-control'
		form.fields['start_time'].widget.attrs['readonly'] = '1'
		
		form.fields['end_time'].widget.attrs['class'] = 'form-control'
		form.fields['end_time'].widget.attrs['readonly'] = '1'

		form.fields['register_start_time'].widget.attrs['class'] = 'form-control'
		form.fields['register_start_time'].widget.attrs['readonly'] = '1'

		form.fields['register_end_time'].widget.attrs['class'] = 'form-control'
		form.fields['register_end_time'].widget.attrs['readonly'] = '1'

		form.fields['register_state'].widget.attrs['class'] = 'form-control'
		form.fields['published'].widget.attrs['class'] = 'form-control'
		
		return form



# Khung nhìn tạo một hoạt động
class ActivityCreateView(CreateView, BaseActivityFormView):
	model = Activity

#	form_class = ActivityForm

	template_name = 'v1/activity/activity_create.html'

	success_message = u'Thêm hoạt động thành công'

	def get_success_url(self):
		return reverse('activity_list_view_v1')

	def get_form(self, form_class):
		kwargs = self.get_form_kwargs()

		params = {}
		params['user_id'] = self.request.session['user_id']
		
		return form_class(params, **kwargs)


	def form_valid(self, form):
		self.object = form.save(commit=False)
		return super(ActivityCreateView, self).form_valid(form)





class BaseActivityUpdateView(UpdateView, BaseActivityFormView):
	model = get_activity_model()
	fields= '__all__'
	success_message = u'Cập nhật thông tin thành công'

	def get_context_data(self, **kwargs):
		context = super(BaseActivityUpdateView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin hoạt động'
		context['page_title'] = u'Thông tin hoạt động'
		
		context['activity_active'] = 'active'

		context['member_full_name'] = self.object.get_full_name()

		return context


class ActivityUpdateView(BaseActivityUpdateView):
	template_name = 'v1/user/user_update.html'

	def get_success_url(self):
		return reverse('activity_update_view_v1', kwargs={'activity_id' : self.kwargs['activity_id'] })

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.creator = self.request.activity
		self.object.status = 0

		activity_id = self.request.session['activity_id']
		user = self.kwargs['activity_id']

		# if int(activity) == user_id:
		# 	self.request.session['activity_full_name'] = self.object.get_full_name()
		
		self.object.save()

		self.clear_messages()

		return super(ActivityUpdateView, self).form_valid(form)

	def get_object(self):
		try:
			return set_activity(	self.request.session['activity_id'],
							self.kwargs['activity_id']
						)

		except:
			raise Http404('Activity does not exist!')


class ActivityMemberImportView(BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = ['activity_identify', 'user_identify']
	
	def get_success_url(self):
		return reverse('organization_tree_view_v1')

	def input_row(self, row):
		try:
			for field in self.CONST_FIELDS:
				print row[field]
		except Exception as e:
			return e
		
		identify = row['identify']
		name = row['name']
		organization_type = row['organization_type']

		create_organization_by_infomation(	self.request.session['user_id'],
											identify,
											name,
											organization_type	)

		print '-------------'
		return 'ok'
