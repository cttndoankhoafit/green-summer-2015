# -*- coding: utf-8 -*-

from django.utils.html import mark_safe

from mms_backoffice.models import *
from django.views.generic import TemplateView

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

#nedregion
