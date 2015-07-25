# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied

from django.views.generic import CreateView, ListView,TemplateView,DetailView, UpdateView

from django.utils.html import mark_safe

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from mms_controller.resources_temp import *


success_add_organization_type_message = u'Thêm loại tổ chức thành công'
success_update_organization_type_message = u'Cập nhật loại tổ chức thành công'



# Khung nhìn xem thông tin của một loại tổ chức
# URL: organization_type/organization_type=<organization_type_id>/
class OrganizationTypeDetailView(TemplateView):
	template_name = 'temporary/base.html'


# Khung nhìn lấy danh sách các loại tổ chức
# URL: organization-type/list/
class OrganizationTypeListView(ListView):
	template_name = 'v1/list.html'
	paginate_by = '20'

	can_set = False

	def get_context_data(self, **kwargs):
		context = super(OrganizationTypeListView, self).get_context_data(**kwargs)
		
		context['title'] = u'Danh sách loại tổ chức'
		context['page_title'] = u'Danh sách loại tổ chức'

		context['organization_active'] = 'active'
		context['organization_type_list_active'] = 'active'

		context['import_link'] = 'import/'
		context['theads'] = []

		if self.can_set:
			context['theads'].append({'name': u'Mã loại tổ chức', 'size' : '20%'})
			context['can_set_list'] = 1

		context['theads'].append({'name': u'Tên loại tổ chức', 'size' : 'auto'})
		context['theads'].append({'name': '', 'size' : '8%'})
			
		# context['add_link'] = '/organization/create/'
		# context['import_link'] = '/organization/import/'

		return context

	def get_queryset(self):
		organization_type_list = get_organization_type_list(self.request.session['user_id'])

		self.can_set = False # can_set_organization_type(self.request.session['user_id'])
		objects = []
		for obj in organization_type_list:
			values =[]
			if self.can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.identify))
				values.append(obj.identify)
			values.append(obj.name)
			values.append(mark_safe(u'<a href="/organization_type/organization_type=%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.identify)))
			objects.append(values)

		return objects



# Khung nhìn cập nhật loại tổ chức
# URL: organization_type/organization_type=<organization_type_id>/
class OrganizationTypeUpdateView(BaseSuccessMessageMixin, UpdateView):
	template_name = 'temporary/editor.html'
	fields = '__all__'

	success_message = success_update_organization_type_message

	def get_success_url(self):
		return reverse('organization_type_update_view_v1', kwargs={'organization_type_id' : self.kwargs['organization_type_id']})
	
	def form_valid(self,form):
		self.object = form.save(commit=False)

		if set_organization_type(self.request.session['user_id'], self.object):
			self.clear_messages()
			return super(OrganizationTypeUpdateView, self).form_valid(form)

	def get_object(self):
		if not is_super_administrator_id(self.request.session['user_id']):
			raise PermissionDenied
		organization_type = get_organization_type(self.request.session['user_id'], self.kwargs['organization_type_id'])
		return organization_type



# Khung nhìn tạo một loại tổ chức dành cho người quản trị hệ thống
# URL: organization_type/create/
class OrganizationTypeCreateView(BaseSuccessMessageMixin, CreateView):
	template_name = 'temporary/editor.html'
	#form_class = OrganizationTypeForm
	model = get_organization_type_model()	
	fields = '__all__'
	
	def get_success_url(self):
		return reverse('organization_type_list_view_v1')

	def get_context_data(self, **kwargs):
		context = super(OrganizationTypeCreateView, self).get_context_data(**kwargs)
		if not is_super_administrator_id(self.request.session['user_id']):
			raise PermissionDenied

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		
		if set_organization_type(self.request.session['user_id'], self.object):
			self.clear_messages()
			return super(OrganizationTypeCreateView, self).form_valid(form)



# Khung nhìn nhập danh sách loại tổ chức dành cho người quản trị hệ thống
# URL: organization_type/import/
class OrganizationTypeImportView(BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = (	'identify',
						'name',
						'management_level'	)

	def get_success_url(self):
		return reverse('organization_type_list_view_v1')

	def input_row(self, row):
		try:
			for field in self.CONST_FIELDS:
				print row[field]
		except Exception as e:
			return e
		
		identify = row['identify']
		name = row['name']
		management_level = row['management_level']

		create_organization_type_by_infomation(	self.request.session['user_id'],
											identify,
											name,
											management_level	)

		print '-------------'
		return 'ok'


	