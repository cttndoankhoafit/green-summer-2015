# -*- coding: utf-8 -*-

from django.views.generic import CreateView, ListView

from django.utils.html import mark_safe

from mms_controller.resources.organization_type import *

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from django.core.urlresolvers import reverse

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

class OrganizationTypeCreateView(CreateView):
	template_name = 'temporary/organization_type/editor.html'
	#form_class = OrganizationTypeForm
	model = get_organization_type_model()	
	fields = ['name']
	
	# def form_valid(self, form):
	# 	form.submit()
	# 	return super(OrganizationTypeCreateView, self).form_valid(form)


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


	