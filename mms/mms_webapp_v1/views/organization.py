# -*- coding: utf-8 -*-

from django.utils.html import mark_safe

from mms_backoffice.models import *
from django.views.generic import TemplateView, CreateView, ListView, DetailView

from django.http import HttpResponseRedirect, HttpResponse

from mms_controller.resources.organization import *

from django.core.urlresolvers import reverse_lazy, reverse

#region GET UNDER ORGANIZATION

class OrganizationOrganizationView(TemplateView):
	template_name = 'v1/tree.html'

	def get_context_data(self, **kwargs):
		context = super(OrganizationOrganizationView, self).get_context_data(**kwargs)
		
		identify = self.kwargs['organization_id']

		org =  Organization.objects.get(id=identify)

		if org is not None:
			context['html_content'] = mark_safe('<ul><li>' + org.name + self.toHtml(self.get_org_list(identify)) + '</li></ul>')
		
		# print context['html_content']

		return context

	def get_org_list(self, organization_id):
		managed_list = Organization.objects.filter(organization_manager=organization_id)
		res = []
		if len(managed_list) == 0:
			return res

		# for i in managed_list:
		# 	res.append((i.organization_managed, i.organization_manager.id, ))
		# 	res.append(self.get_org_list(i.organization_managed.id))

		for i in managed_list:
			res.append(i)
			res.append(self.get_org_list(i.id))

		return res

	def toHtml(self, objects):
		html = u''
		if (type(objects) is list) and (len(objects) == 0):
			return html

		if type(objects) is list:
			html += u'<ul>\n'
			for o in objects:
				html += self.toHtml(o)
			html += u'</ul>\n'
			return html

		html += u'<li>\n'
		html += objects.name + u'\n'
		return html

#endregion

#region GET ALL ORGANIZATIONS THAT USER user_id MANAGE

class UserOrganizationView(TemplateView):
	template_name = 'v1/tree.html'

	def get_context_data(self, **kwargs):
		context = super(UserOrganizationView, self).get_context_data(**kwargs)
		identify = self.kwargs['user_id']
		orgs = OrganizationUser.objects.filter(user__id=identify, state=0)
		res = []
		for i in orgs:
			res.append(i.organization)
			res.append(self.get_org_list(i.organization.id))

		context['html_content'] = self.toHtml(res)

		return context

	def get_org_list(self, organization_id):
		managed_list = Organization.objects.filter(organization_manager=organization_id)
		res = []
		if len(managed_list) == 0:
			return res

		for i in managed_list:
			res.append(i)
			res.append(self.get_org_list(i.id))

		return res

	def toHtml(self, objects):
		html = ""
		if (type(objects) is list) and (len(objects) == 0):
			return html

		if type(objects) is list:
			html += "<ul>\n"
			for o in objects:
				html += self.toHtml(o)
			html += "</ul>\n"
			return html

		html += "<li>\n"
		html += objects.name + "\n"
		return html

class OrganizationCreateView(CreateView):
	model = Organization
	fields = '__all__'

	template_name = 'v1/organization/editor.html'# template of OrganizationCreateView is the same as UserCreateView

 	def get_form(self, form_class):
		form = super(OrganizationCreateView, self).get_form(form_class)
		return form

	def form_valid(self,form):
		self.object = form.save(commit=False)
		print self.object
		if create_organization(self.request.session['user_id'], self.object):
			return HttpResponse(reverse('organization_list_view_v1'))
#nedregion


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

		can_get_managed_organization = can_get_managed_organization_list(user_id)

		if can_get:
			organization_list = get_organization_list(user_id)
		else:
			if can_get_managed_organization:
				organization_list = get_managed_organization_list(user_id)

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
		
		org = Organization.objects.get(name='root')


		if org is not None:
			context['html_content'] = mark_safe(self.toHtml(self.get_org_list(org.id)))

		if can_create_organization(self.request.session['user_id']):
			context['can_create_organization'] = 1

		return context

	def get_org_list(self, organization_id):
		managed_list = Organization.objects.filter(organization_manager=organization_id)
		res = []
		if len(managed_list) == 0:
			return res

		# for i in managed_list:
		# 	res.append((i.organization_managed, i.organization_manager.id, ))
		# 	res.append(self.get_org_list(i.organization_managed.id))

		for i in managed_list:
			res.append(i)
			res.append(self.get_org_list(i.id))

		return res

	def toHtml(self, objects):
		html = u''
		if (type(objects) is list) and (len(objects) == 0):
			return html

		if type(objects) is list:
			html += u'<ul>\n'
			for o in objects:
				html += self.toHtml(o)
			html += u'</ul>\n'
			return html

		html += u'<li>\n'
		html += objects.name + u'\n'
		return html

class OrganizationDetailView(DetailView):
	template_name = 'v1/organization/organization_overview.html'

	def get_object(self):
		return get_organization(	self.request.session['user_id'],
									self.kwargs['organization_id']
								)