# -*- coding: utf-8 -*-

from django.views.generic import ListView, CreateView

from django.utils.html import mark_safe

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from django.core.urlresolvers import reverse

from mms_webapp_v1.views.bases.base_view import *

from mms_base.resources import *

success_add_organization_type_message = u'Thêm loại hoạt động thành công'
success_update_organization_type_message = u'Cập nhật loại hoạt động thành công'

class BaseActivityTypeView(BaseView):
	def get_context_data(self, **kwargs):
		if not is_super_administrator(self.get_user_id()):
			raise PermissionDenied
		context = super(BaseActivityTypeView, self).get_context_data(**kwargs)
		return context

		
class ActivityTypeListView(BaseActivityTypeView, ListView):
	template_name = 'v1/static_pages/list.html'
	paginate_by = '20'


	def get_context_data(self, **kwargs):
		context = super(ActivityTypeListView, self).get_context_data(**kwargs)
		
		context['title'] = u'Danh sách loại hoạt động'
		context['page_title'] = u'Danh sách loại hoạt động'

		context['activity_active'] = 'active'
		context['activity_type_list_active'] = 'active'

		context['show_add_button'] = 1
		context['show_delete_button'] = 1
		context['show_import_button'] = 1
		context['show_checkbox'] = 1

		context['add_link'] = '/activity_type/create/'
		context['import_link'] = '/activity_type/import/'
		context['theads'] = []

		context['theads'] = [	{'name': u'#', 'size' : '10%'}, 
								{'name': u'Tên loại hoạt động', 'size' : 'auto'}	]
		
		context['can_set'] = 1

		return context

	def get_queryset(self):
		activity_type_list = get_activity_type_list()

		objects = []
		for obj in activity_type_list:
			values =[]
			values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.identify))
			values.append(obj.identify)
			values.append(mark_safe(u'<a href="/activity_type/activity_type=%s/edit/">%s</a>' % (obj.identify, obj.name)))
			objects.append(values)

		return objects



class BaseActivityTypeFormView(BaseActivityTypeView, BaseSuccessMessageMixin, FormView):
	def get_form(self, form_class):
		form = super(BaseActivityTypeFormView, self).get_form(form_class)
		if 'identify' in form.fields:
			form.fields['identify'].widget.attrs['class'] = 'form-control'
		form.fields['name'].widget.attrs['class'] = 'form-control'
		
		return form



class ActivityTypeCreateView(BaseActivityTypeFormView, CreateView):
	model = get_activity_type_model()

	fields =[	'identify',
				'name',
			]

	template_name = 'v1/activity_type/creator.html'

	success_message = u'Thêm loại hoạt động thành công'

	def get_context_data(self, **kwargs):
		context = super(ActivityTypeCreateView, self).get_context_data(**kwargs)
		context['page_title'] = u'Thêm loại hoạt động'
		return context

	def get_success_url(self):
		return reverse('activity_type_list_view_v1')

 	def get_form(self, form_class):
		form = super(ActivityTypeCreateView, self).get_form(form_class)
		return form

	def form_valid(self, form):
		self.object = form.save(commit=False)
		return super(ActivityTypeCreateView, self).form_valid(form)



class ActivityTypeImportView(BaseActivityTypeView, BaseImportView):
	template_name = 'v1/activity_type/import.html'

	CONST_FIELDS = ['identify', 'name']

	def get_context_data(self, **kwargs):
		context = super(ActivityTypeImportView, self).get_context_data(**kwargs)

		context['activity_active'] = 'active'
		context['activity_type_list_active'] = 'active'

		context['page_title'] = 'Thêm loại hoạt động'

		return context

	def get_success_url(self):
		return reverse('activity_type_list_view_v1')

	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		identify = row['identify']
		name = row['name']
		
		set_activity_type(self.get_user_id(), identify, name)

		print '-------------'
		return 'ok'


# class ActivityTypeCreateView(CreateView, ActivityTypeFormView):
# 	model = ActivityType

# 	fields =[	'identify',
# 				'name',
# 			]

# 	template_name = 'v1/activity_type_create.html'

# 	success_message = u'Thêm loại hoạt động thành công'

# 	def get_success_url(self):
# 		return reverse('activity_type_list_view_v1')

#  	def get_form(self, form_class):
# 		form = super(ActivityTypeCreateView, self).get_form(form_class)
# 		return form

# 	def form_valid(self, form):
# 		self.object = form.save(commit=False)
# 		return super(ActivityTypeCreateView, self).form_valid(form)