# -*- coding: utf-8 -*-

from django.views.generic import ListView, CreateView

from django.utils.html import mark_safe

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_controller.resources.activity_type import *

from django.core.urlresolvers import reverse

class ActivityTypeListView(ListView):
	template_name = 'v1/list.html'
	paginate_by = '20'

	can_set = False

	def get_context_data(self, **kwargs):
		context = super(ActivityTypeListView, self).get_context_data(**kwargs)
		
		context['title'] = u'Danh sách loại hoạt động'
		context['page_title'] = u'Danh sách loại hoạt động'

		context['activity_active'] = 'active'
		context['activity_type_list_active'] = 'active'

		context['add_link'] = '/activity_type/create/'
		context['import_link'] = 'import/'
		context['theads'] = []

		if self.can_set:
			context['theads'].append({'name': u'Mã loại hoạt động', 'size' : '20%'})
			context['can_set_list'] = 1

		context['theads'].append({'name': u'Tên loại hoạt động', 'size' : 'auto'})
		context['theads'].append({'name': '', 'size' : '8%'})
			
		# context['add_link'] = '/organization/create/'
		# context['import_link'] = '/organization/import/'

		return context

	def get_queryset(self):
		activity_type_list = get_activity_type_list()

		self.can_set = can_set_activity_type(self.request.session['user_id'])
		objects = []
		for obj in activity_type_list:
			values =[]
			if self.can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.id))
				values.append(obj.identify)
			values.append(obj.name)
			values.append(mark_safe(u'<a href="/activity_type/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.id)))
			objects.append(values)

		return objects


class ActivityTypeImportView(BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = (	'identify',
						'name',
					)

	def get_context_data(self, **kwargs):
		context = super(ActivityTypeImportView, self).get_context_data(**kwargs)

		context['activity_active'] = 'active'
		context['activity_type_list_active'] = 'active'

		return context

	def get_success_url(self):
		return reverse('activity_type_list_view_v1')

	def input_row(self, row):
		try:
			for field in self.CONST_FIELDS:
				print row[field]
		except Exception as e:
			return e
		
		identify = row['identify']
		name = row['name']
		
		create_activity_type_by_infomation(	self.request.session['user_id'],
											identify,
											name, )

		print '-------------'
		return 'ok'

class ActivityTypeFormView(BaseSuccessMessageMixin, FormView):
	def get_form(self, form_class):
		form = super(ActivityTypeFormView, self).get_form(form_class)
		form.fields['identify'].widget.attrs['class'] = 'form-control'
		form.fields['name'].widget.attrs['class'] = 'form-control'

		return form
class ActivityTypeCreateView(CreateView, ActivityTypeFormView):
	model = ActivityType

	fields =[	'identify',
				'name',
			]

	template_name = 'v1/activity_type_create.html'

	success_message = u'Thêm loại hoạt động thành công'

	def get_success_url(self):
		return reverse('activity_type_list_view_v1')

 	def get_form(self, form_class):
		form = super(ActivityTypeCreateView, self).get_form(form_class)
		return form

	def form_valid(self, form):
		self.object = form.save(commit=False)
		return super(ActivityTypeCreateView, self).form_valid(form)