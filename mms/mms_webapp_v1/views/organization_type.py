# -*- coding: utf-8 -*-

from django.views.generic import CreateView, ListView,TemplateView,DetailView, UpdateView, FormView

from django.utils.html import mark_safe

from mms_controller.resources.organization_type import *

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
success_update_organization_type_message = u'Thêm loại tổ chức thành công'

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
			
		context['add_link'] = '/organization_type/create/'
		# context['import_link'] = '/organization/import/'

		return context

	def get_queryset(self):
		organization_type_list = get_organization_type_list()

		self.can_set = can_set_organization_type(self.request.session['user_id'])
		objects = []
		for obj in organization_type_list:
			values =[]
			if self.can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.id))
				values.append(obj.identify)
			values.append(obj.name)
			values.append(mark_safe(u'<a href="/organization_type/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.id)))
			objects.append(values)

		return objects

class BaseOrganizationTypeUpdateView(UpdateView,OrganizationTypeListView):
	model = get_organization_type_model
	field = '__all__'

	success_message = success_update_organization_type_message

	def get_context_data(self, **kwargs):
		context = super(BaseOrganizationTypeUpdateView, self).get_context_data(**kwargs)

		context['title'] = u'Tên loại tổ chức'
		context['page_title'] = u'Tên loại tổ chức'
		context['organization_active'] = 'active'
		#context['organization_'] =

		return context
class OrganizationTypeUpdateView(BaseOrganizationTypeUpdateView):
	template_name = 'v1/import.html'

	def get_sucess_url(self):
		return reverse('organization_type_update_view_v1', kwargs={'organization_type_id' :self.kwargs['organization_type_id']})
	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.creator = self.request.user
		self.object.status = 0

		organization_type_id = self.request.session['organization_type_id']
		organization_type = self.kwargs['organization_type_id']

		self.object.save()
		self.clear_messages()

		return super(OrganizationTypeUpdateView,self).form_valid(form)

	def get_object(self):
		try:
			return set_organization(self.request.session['organization_type_id'],
								self.kwargs['organization_type_id'])

		except:
			raise Http404('Organization Type does not exist!')

# class OrganizationTypeCreateView(CreateView):
# 	template_name = 'temporary/organization_type/editor.html'
# 	#form_class = OrganizationTypeForm
# 	model = get_organization_type_model()	
# 	fields = ['name']
	
# 	# def form_valid(self, form):
# 	# 	form.submit()
# 	# 	return super(OrganizationTypeCreateView, self).form_valid(form)


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

class OrganizationTypeFormView(BaseSuccessMessageMixin, FormView):
	def get_form(self, form_class):
		form = super(OrganizationTypeFormView, self).get_form(form_class)
		form.fields['identify'].widget.attrs['class'] = 'form-control'
		form.fields['name'].widget.attrs['class'] = 'form-control'
		form.fields['management_level'].widget.attrs['class'] = 'form-control'
		form.fields['details'].widget.attrs['class'] = 'form-control'

		return form
class OrganizationTypeCreateView(CreateView, OrganizationTypeFormView):
	model = OrganizationType

	fields =[	'identify',
				'name',
				'management_level',
				'details',
			]

	template_name = 'v1/organization_type_create.html'

	success_message = u'Thêm loại tổ chức thành công'

	def get_success_url(self):
		return reverse('organization_type_list_view_v1')

 	def get_form(self, form_class):
		form = super(OrganizationTypeCreateView, self).get_form(form_class)
		return form

	def form_valid(self, form):
		self.object = form.save(commit=False)
		return super(OrganizationTypeCreateView, self).form_valid(form)
	