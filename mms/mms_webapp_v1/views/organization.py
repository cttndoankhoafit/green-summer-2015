# -*- coding: utf-8 -*-

from django.utils.html import mark_safe

from mms_backoffice.models import *
from django.views.generic import TemplateView, CreateView, ListView, DetailView

from django.http import HttpResponseRedirect, HttpResponse, Http404

from mms_controller.resources.organization import *

from django.core.urlresolvers import reverse_lazy, reverse

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

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

	fields = [	'identify',
				'name',
				'organization_type',
				'manager_organization'	]

	template_name = 'v1/organization/organization_editor.html'# template of OrganizationCreateView is the same as UserCreateView

	success_message = u'Thêm tổ chức thành công'

	def get_success_url(self):
		return reverse('organization_list_view_v1')

	def get_context_data(self, **kwargs):
		context = super(OrganizationCreateView, self).get_context_data(**kwargs)
		
		context['title'] = u'Thêm tổ chức'

		context['page_title'] = u'Thêm tổ chức'

		context['organization_active'] = 'active'
		
		context['button_name'] = u'Thêm tổ chức'

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		if create_organization(self.request.session['user_id'], self.object):
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

		if self.can_set:
			context['can_set_list'] = 1

		return context

	def get_queryset(self):
		user_id = self.request.session['user_id']
		organization_list = None

		self.can_set = can_set_organization_list(user_id)

		can_get = can_get_organization_list(user_id)

		organization_list = get_organization_list(user_id)
		
		objects = []
		if organization_list is not None:
			for obj in organization_list:
				values = []
				if self.can_set:
					values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.id))
				values.append(obj.name)
				values.append(mark_safe(u'<a href="/organization/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.id)))
				objects.append(values)

		return objects

class OrganizationTreeView(TemplateView):
	template_name = 'v1/organization/organization_tree.html'

	def get_context_data(self, **kwargs):
		context = super(OrganizationTreeView, self).get_context_data(**kwargs)
		
		org = get_organization_root()

		context['organization_active'] = 'active'
		context['organization_tree_active'] = 'active'

		context['tree_content'] = mark_safe(self.toHtml(get_organization_tuple_table(self.request.session['user_id'], get_organization_root()))
		)

		if can_manage_organization(self.request.session['user_id']):
			context['can_manage_organization'] = 1

		return context

	def toHtml(self, table):
		html = ''
		if len(table[1]) > 0:
			html += '<ul>'
			for obj in table[1]:
				html += '<li><a href="/organization/%s/">' % obj[0].id
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
						'organization_type'	)

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

class OrganizationManagementImportView(BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = (	'manager_organization',
						'managed_organization'	)

	def get_success_url(self):
		return reverse('organization_tree_view_v1')

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



class OrganizationDetailView(DetailView):
	template_name = 'v1/organization/organization_overview.html'

	def get_context_data(self, **kwargs):
		context = super(OrganizationDetailView, self).get_context_data(**kwargs)
		
		context['organization_id'] = self.kwargs['organization_id']

		context['overview_active'] ='active'

		context['organization_name'] = self.object.name

		return context

	def get_object(self):
		try:
			return get_organization(	self.request.session['user_id'],
									self.kwargs['organization_id']
								)
		except:
			raise Http404('Organization does not exist!')

class UnderOrganizationTreeView(TemplateView):
	template_name = 'v1/organization/organization_under.html'

	def get_context_data(self, **kwargs):
		context = super(UnderOrganizationTreeView, self).get_context_data(**kwargs)
		
		org = get_organization_root()

		context['organization_active'] = 'active'
		
		context['organization_name'] = get_organization(self.request.session['user_id'], self.kwargs['organization_id']).name

		context['tree_content'] = mark_safe(self.toHtml(get_organization_tuple_table_by_id(self.request.session['user_id'],  self.kwargs['organization_id']))
		)

		context['under_organizations_active'] = 'active'
		
		if can_manage_organization(self.request.session['user_id']):
			context['can_manage_organization'] = 1

		return context

	def toHtml(self, table):
		html = ''
		if len(table[1]) > 0:
			html += '<ul>'
			for obj in table[1]:
				html += '<li><a href="/organization/%s/">' % obj[0].id
				html += obj[0].name
				html += '</a>'
				html += self.toHtml(obj)
				html += '</li>'
			html += '</ul>'
		return html

class OrganizationMemberListView(ListView):
	template_name = 'v1/organization/organization_member.html'
	paginate_by = '20'

	can_set = False

	def get_context_data(self, **kwargs):
		context = super(OrganizationMemberListView, self).get_context_data(**kwargs)
		
		org = get_organization_root()

		context['organization_id'] = self.kwargs['organization_id']

		context['theads'] = [	{'name': u'Mã số', 'size' : '20%'},
								{'name': u'Họ và Tên', 'size' : 'auto'},
								{'name': '', 'size' : '8%'},	]

		context['members_active'] ='active'

		context['import_link'] = 'import/'

		if self.can_set:
			context['can_set_list'] = 'active'

		try:
			context['organization_name'] = get_organization(self.request.session['user_id'], self.kwargs['organization_id']).name
		except:
			raise Http404('Organization does not exist!')
		return context

	def get_queryset(self):
		user_list = get_organization_user_list(self.request.session['user_id'], self.kwargs['organization_id'])

		self.can_set = is_organization_administrator(self.request.session['user_id'], self.kwargs['organization_id'])
		objects = []
		for obj in user_list:
			values = []
			if self.can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="%s" name="list"/>' % obj.id))
			values.append(obj.identify)
			values.append(obj.get_full_name())
			values.append(mark_safe(u'<a href="/user/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.id)))
			objects.append(values)
		return objects



class OrganizationMemberImportView(BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = ('user_identify')

	def get_context_data(self, **kwargs):
		context = super(OrganizationMemberImportView, self).get_context_data(**kwargs)
		
		org = get_organization_root()

		context['organization_id'] = self.kwargs['organization_id']

		context['members_active'] ='active'

		try:
			context['organization_name'] = get_organization(self.request.session['user_id'], self.kwargs['organization_id']).name
		except:
			raise Http404('Organization does not exist!')
		return context

	def get_success_url(self):
		return reverse('organization_member_list_view_v1', kwargs={ 'organization_id' : self.kwargs['organization_id']  })

	def input_row(self, row):
		# try:
		# 	for field in self.CONST_FIELDS:
		# 		print row[field]
		# except Exception as e:
		# 	print e
		# 	return e
		
		organization_identify = get_organization(self.request.session['user_id'], self.kwargs['organization_id']).identify
		user_identify = row['user_identify']
		
		add_organization_user_by_identify(	self.request.session['user_id'],
											organization_identify,
											user_identify	)

		print '-------------'
		return 'ok'
