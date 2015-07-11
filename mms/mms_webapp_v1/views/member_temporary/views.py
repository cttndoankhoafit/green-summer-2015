from django.views.generic import ListView

from mms_backoffice.models import *

class OrganizationMemberListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	def get_queryset(self):
		identify = self.kwargs['organization_id']
		org_list = self.get_org_list(identify)
		return org_list
		res = set([i.member for i in OrganizationMember.objects.filter(organization=identify)])

		for org in org_list:
			tmp = OrganizationMember.objects.filter(organization=org.id)
			memlist = set([i.member for i in tmp])
			res = res|memlist
		return list(res)

	def get_org_list(self, org_id):
		managed_list = OrganizationManager.objects.filter(organization_manager=org_id)
		res = []
		if len(managed_list) == 0:
			return res

		for i in managed_list:
			res.append(i.organization_managed)
			res += (self.get_org_list(i.organization_managed.id))

		return res

#member managed by user 

class UserMemberListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	def get_queryset(self): 
		identify = self.kwargs['user_id']
		orgs = OrganizationUserManager.objects.filter(user__id=identify)
		org_list = []
		for i in orgs:
			org_list.append((i.organization))
			org_list += self.get_org_list(i.organization.id)
		res = set([i.member for i in OrganizationMember.objects.filter(organization=identify)])

		for org in org_list:
			tmp = OrganizationMember.objects.filter(organization=org.id)
			memlist = set([i.member for i in tmp])
			res = res|memlist
		return list(res)

	def get_org_list(self, org_id):
		managed_list = OrganizationManager.objects.filter(organization_manager=org_id)
		res = []
		if len(managed_list) == 0:
			return res

		for i in managed_list:
			res.append(i.organization_managed)
			res += (self.get_org_list(i.organization_managed.id))

		return res