# -*- coding: utf-8 -*-

from django.utils.html import mark_safe
from django.core.urlresolvers import reverse
from django.views.generic import ListView, UpdateView, TemplateView, DetailView, CreateView, View
from django.http import HttpResponseRedirect, Http404

from mms_backoffice.models import Activity, ActivityUser

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_controller.resources.activity import *
from mms_controller.resources_temp import *

from mms_webapp_v1.forms.activity import ActivityForm


class BaseActivityView(View):
	def get_context_data(self, **kwargs):
		context = super(BaseActivityView, self).get_context_data(**kwargs)

		context['activity_id'] = self.kwargs['activity_id']

		return context
		

class ActivityListView(ListView):
	template_name = 'v1/list.html'
	paginate_by = '20'

	can_set = True

	def get_context_data(self, **kwargs):
		context = super(ActivityListView, self).get_context_data(**kwargs)

		context['title'] = u'Danh sách hoạt động'
		context['page_title'] = u'Danh sách hoạt động'

		context['activity_active'] = 'active'
		context['activity_list_active'] = 'active'

		context['theads'] = [	{'name': u'Tên hoạt động', 'size' : 'auto'},
								{'name': u'Loại hoạt động', 'size' : '15%'},
								{'name': u'Thời gian tổ chức', 'size' : '15%'},
								# {'name': u'Trạng thái', 'size' : 'auto'},
								{'name': u'', 'size' : '15%'},
							]
		context['add_link'] = '/activity/create/'

		if self.can_set:
			context['can_set_list'] = 1

		return context

	def get_color(self, value):
		if value == 0:
			return 'blue'
		elif value == 1:
			return 'green'
		elif value == 2:
			return 'purple'

	def get_queryset(self):
		activity_list = get_activity_list(self.request.session['user_id'])

		objects = []
		for obj in activity_list:
			values = []
			if self.can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.identify))
			values.append(obj.name)
			values.append(obj.activity_type)
			values.append(obj.start_time)
			buttons = ''
			if obj.register_state < 3:
				buttons += u'<a class="btn default btn-xs green-stripe">Đăng ký</a>'
			buttons += u'<a href="/activity/activity=%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % obj.identify
			values.append(mark_safe(buttons))

			objects.append(values)
		return objects

class ActivityDetailView(BaseActivityView, DetailView):
	template_name = 'v1/activity/activity_overview.html'

	def get_object(self):
		return get_activity(self.kwargs['activity_id'])

class ActivityMemberListView(BaseActivityView, ListView):
	template_name = 'v1/activity/activity_member.html'
	paginate_by = '20'

	def get_queryset(self):

		return []


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

	form_class = ActivityForm

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
