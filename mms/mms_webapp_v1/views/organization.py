from mms_backoffice.models import *
from django.views.generic import TemplateView

#region GET UNDER ORGANIZATION

class OrganizationOrganizationView(TemplateView):
	template_name = 'temporary/treeview/treeView.html'
	rootID = 0

	def get_context_data(self, **kwargs):
		context = super(OrganizationOrganizationView, self).get_context_data(**kwargs)
		
		identify = self.kwargs['organization_id']
		self.rootID = identify
		context['html_content'] = 'foldersTree = gFld(\"%s\")\n' % Organization.objects.get(id=identify).name
		context['html_content'] += self.toHtml(self.get_org_list(identify))
		
		return context

	def get_org_list(self, organization_id):
		managed_list = OrganizationManager.objects.filter(organization_manager=organization_id)
		res = []
		if len(managed_list) == 0:
			return res

		for i in managed_list:
			res.append((i.organization_managed, i.organization_manager.id, ))
			res.append(self.get_org_list(i.organization_managed.id))

		return res

	def toHtml(self, objects):
		html = ""
		if (type(objects) is list) and (len(objects) == 0):
			return html

		if type(objects) is list:
			#html += "<ul>\n"
			for o in objects:
				html += self.toHtml(o)
			#html += "</ul>\n"
			return html

		#html += "<li>"
		#html += objects[0].name
		#html += "</li>\n"
		if objects[1] == int(self.rootID):
			html += 'aux%d = insFld(foldersTree, gFld("%s"))\n' % (objects[0].id, objects[0].name)
		else:
			html += 'aux%d = insFld(aux%d, gFld("%s"))\n' % (objects[0].id, objects[1], objects[0].name)
		return html

#endregion

#region GET ALL ORGANIZATIONS THAT USER user_id MANAGE

class UserOrganizationView(TemplateView):
	template_name = 'temporary/treeview/treeView.html'

	def get_context_data(self, **kwargs):
		context = super(UserOrganizationView, self).get_context_data(**kwargs)
		identify = self.kwargs['user_id']
		orgs = OrganizationUserManager.objects.filter(user__id=identify)
		res = []
		for i in orgs:
			res.append((i.organization, 0, ))
			res.append(self.get_org_list(i.organization.id))

		context['html_content'] = 'foldersTree = gFld(\"%s\")\n' % User.objects.get(id=identify).username
		context['html_content'] += self.toHtml(res)
		return context

	def get_org_list(self, org_id):
		managed_list = OrganizationManager.objects.filter(organization_manager=org_id)
		res = []
		if len(managed_list) == 0:
			return res

		for i in managed_list:
			res.append((i.organization_managed, i.organization_manager.id, ))
			res.append(self.get_org_list(i.organization_managed.id))

		return res

	def toHtml(self, objects):
		html = ""
		if (type(objects) is list) and (len(objects) == 0):
			return html

		if type(objects) is list:
			#html += "<ul>\n"
			for o in objects:
				html += self.toHtml(o)
			#html += "</ul>\n"
			return html

		#html += "<li>"
		#html += objects[0].name
		#html += "</li>\n"
		if objects[1] == 0:
			html += 'aux%d = insFld(foldersTree, gFld("%s"))\n' % (objects[0].id, objects[0].name)
		else:
			html += 'aux%d = insFld(aux%d, gFld("%s"))\n' % (objects[0].id, objects[1], objects[0].name)
		return html

#nedregion
