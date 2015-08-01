# -*- coding: utf-8 -*-


from django.core.exceptions import PermissionDenied

from django.views.generic import CreateView, ListView,TemplateView,DetailView, UpdateView

from django.utils.html import mark_safe

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse

from mms_webapp_v1.views.bases.base_view import *

from mms_base.resources import *

success_add_organization_type_message = u'Thêm loại tổ chức thành công'
success_update_organization_type_message = u'Cập nhật loại tổ chức thành công'



# Khung nhìn chung cho quản lý loại tổ chức
class BaseOrganizationTypeView(BaseView):
	def get_organization_type_id(self):
		if 'organization_type_id' in self.kwargs:
			return self.kwargs['organization_type_id']
		return None

	def get_context_data(self, **kwargs):
		if not is_super_administrator(self.get_user_id()):
			raise PermissionDenied
		context = super(BaseOrganizationTypeView, self).get_context_data(**kwargs)

		context['organization_type_id'] = self.get_organization_type_id()
		
		return context




class BaseOrganizationTypeFormView(BaseOrganizationTypeView, BaseSuccessMessageMixin, FormView):
	def get_form(self, form_class):
		form = super(BaseOrganizationTypeFormView, self).get_form(form_class)
		if 'identify' in form.fields:
			form.fields['identify'].widget.attrs['class'] = 'form-control'
		form.fields['name'].widget.attrs['class'] = 'form-control'
		form.fields['management_organzation_type'].widget.attrs['class'] = 'form-control'

		return form



# Khung nhìn cập nhật loại tổ chức
# URL: organization_type/organization_type=<organization_type_id>/
class OrganizationTypeUpdateView(BaseOrganizationTypeFormView, UpdateView):
	template_name = 'v1/organization_type/update.html'

	success_message = success_update_organization_type_message

	fields = ['name', 'management_organzation_type']

	def get_success_url(self):
		return reverse('organization_type_update_view_v1', kwargs={'organization_type_id' : self.get_organization_type_id()})
	
	def get_context_data(self, **kwargs):
		context = super(OrganizationTypeUpdateView, self).get_context_data(**kwargs)
		context['page_title'] = get_organization_type(self.get_organization_type_id()).name
		context['button_value'] = u'Cập nhật'
		
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		set_organization_type(self.get_user_id(), self.object)
		self.clear_messages()
		return super(OrganizationTypeUpdateView, self).form_valid(form)

	def get_object(self):
		return get_organization_type(self.get_organization_type_id())



class OrganizationTypePositionListView(BaseOrganizationTypeView, ListView):
	template_name = 'v1/organization_type/position/list.html'

	def get_context_data(self, **kwargs):
		context = super(OrganizationTypePositionListView, self).get_context_data(**kwargs)

		context['theads'] = [ 	{'name': u'Tên chức vụ', 'size' : 'auto'} ]

		return context

	def get_queryset(self):
		position_list = get_organization_type_position_list(self.get_organization_type_id())

		objects = []
		for obj in position_list:
			values = []
			values.append(obj.name)
			objects.append(values)
		return objects


# Khung nhìn tạo một loại tổ chức dành cho người quản trị hệ thống
# URL: organization_type/create/
class OrganizationTypeCreateView(BaseOrganizationTypeFormView, CreateView):
	model = get_organization_type_model()

	template_name = 'v1/organization_type/creator.html'

	success_message = success_add_organization_type_message

	fields = ['identify', 'name', 'management_organzation_type']

	def get_success_url(self):
	 	return reverse('organization_type_list_view_v1')

	def get_context_data(self, **kwargs):
		context = super(OrganizationTypeCreateView, self).get_context_data(**kwargs)
		context['page_title'] = u'Thêm loại tổ chức'
		context['button_value'] = u'Thêm'
		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		set_organization_type(self.get_user_id(), self.object)
		self.clear_messages()
		return super(OrganizationTypeCreateView, self).form_valid(form)



# Khung nhìn lấy danh sách các loại tổ chức
# URL: organization-type/list/
class OrganizationTypeListView(BaseOrganizationTypeView, ListView):
	template_name = 'v1/static_pages/list.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(OrganizationTypeListView, self).get_context_data(**kwargs)
		
		context['title'] = u'Danh sách loại tổ chức'
		context['page_title'] = u'Danh sách loại tổ chức'

		context['organization_active'] = 'active'
		context['organization_type_list_active'] = 'active'

		context['show_add_button'] = 1
		context['show_delete_button'] = 1
		context['show_import_button'] = 1
		context['show_checkbox'] = 1

		context['theads'] = [ 	{'name': u'#', 'size' : '10%'},
								{'name': u'Tên loại tổ chức', 'size' : 'auto'},
								{'name': u'Tên loại tổ chức quản lý', 'size': 'auto'}]

			
		context['add_link'] = '/organization_type/create/'
		context['import_link'] = '/organization_type/import/'

		return context

	def get_queryset(self):
		organization_type_list = get_organization_type_list()

		self.can_set = False # can_set_organization_type(self.request.session['user_id'])
		objects = []
		for obj in organization_type_list:
			values =[]
			values.append(mark_safe('<input type="checkbox" class="checkboxes" value="%s" name="list"/>' % obj.identify))
			values.append(obj.identify)
			values.append(mark_safe(u'<a href="/organization_type/organization_type=%s/edit/">%s</a>' % (obj.identify, obj.name)))
			organization_type = obj.management_organzation_type
			if organization_type is None:
				values.append('')
			else:
				values.append(mark_safe(u'<a href="/organization_type/organization_type=%s/edit/">%s</a>' % (organization_type.identify, organization_type.name)))
			objects.append(values)

		return objects



# Khung nhìn nhập danh sách loại tổ chức dành cho người quản trị hệ thống
# URL: organization_type/import/
class OrganizationTypeImportView(BaseOrganizationTypeView, BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = (	'identify',
						'name',
						'management_type'	)

	def get_success_url(self):
		return reverse('organization_type_list_view_v1')

	def get_context_data(self, **kwargs):
		context = super(OrganizationTypeImportView, self).get_context_data(**kwargs)
		context['page_title'] = u'Nhập danh sách loại tổ chức'
		return context

	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		identify = row['identify']
		name = row['name']
		management_type = row['management_type']

		set_organization_type(	self.request.session['user_id'],
											identify,
											name,
											management_type	)

		print '-------------'
		return 'ok'


	
