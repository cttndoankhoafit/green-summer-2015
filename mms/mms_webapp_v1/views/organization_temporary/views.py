from django.shortcuts import render, get_object_or_404
from mms_backoffice.models import *
from django.views import generic
from django.views.generic import ListView

class ChildOrganizationListView(generic.View):
	template_name = 'temporary/organization/sub_organization2.html'

	# def get_queryset(self):
	# 	identify = self.kwargs['organization_id']
	# 	objects = self.get_org_list(identify)
	# 	print self.toHtml(objects)

	# 	return self.toHtml(objects)

	def get_context_data(self, **kwargs):
		context = super(ChildOrganizationListView, self).get_context_data(**kwargs)
		identify = self.kwargs['organization_id']
		objects = self.get_org_list(identify)
		context['html_content'] = self.toHtml(objects)
		return context

	def get_org_list(self, org_id):
		managed_list = OrganizationManager.objects.filter(organization_manager=org_id)
		res = []
		if len(managed_list) == 0:
			return res

		for i in managed_list:
			res.append(i.organization_managed)
			res.append(self.get_org_list(i.organization_managed.id))

		return res

	def toHtml(self, objects):
		html = ""
		if (type(objects) is list) and (len(objects) == 0):
			return html

		if type(objects) is list:
			html += "<ul>"
			for o in objects:
				html += self.toHtml(o)
			html += "</ul>"
			return html

		html += "<li>"
		html += objects.name
		html += "</li>"
		return html

"""
    Show all organizations (including child organizations) managed by a user.
"""
class ManagedOrganizationListView(generic.TemplateView):
	template_name = 'temporary/organization/managed_organization2.html'

	def get_queryset(self):
		pass
	#     identify = self.kwargs['user_id']
	#     objs = OrganizationUserManager.objects.filter(user__id=identify)
	#     res = []

	#     for i in objs:
	#     	res.append(i.organization)
	#     	res += self.get_org_list(i.organization.id)

	#     return res

	def get_context_data(self, **kwargs):
		context = super(ManagedOrganizationListView, self).get_context_data(**kwargs)
		identify = self.kwargs['user_id']
		orgs = OrganizationUserManager.objects.filter(user__id=identify)
		res = []
		for i in orgs:
			res.append(i.organization)
			res.append(self.get_org_list(i.organization.id))

		#for i in res:
		#	objects = self.get_org_list(i.id)
		context['html_content'] = self.toHtml(res)
		return context

	def get_org_list(self, org_id):
		managed_list = OrganizationManager.objects.filter(organization_manager=org_id)
		res = []
		if len(managed_list) == 0:
			return res

		for i in managed_list:
			res.append(i.organization_managed)
			res.append(self.get_org_list(i.organization_managed.id))

		return res

	def toHtml(self, objects):
		html = ""
		if (type(objects) is list) and (len(objects) == 0):
			return html

		if type(objects) is list:
			html += "<ul>"
			for o in objects:
				html += self.toHtml(o)
			html += "</ul>"
			return html

		html += "<li>"
		html += objects.name
		html += "</li>"
		return html
#Show organization type
# class OrganizationTypeListView(ListView):
# 	template_name = 'temporary/organization/organization_types.html'
# 	def get_queryset(self):
# 	    objects = OrganizationType.objects.order_by('-name')
# 	    return objects