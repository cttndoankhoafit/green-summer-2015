from mms_backoffice.models import Organization, User, OrganizationUser

#region get_organization_user_manage
def get_organization_user_manage(user_manager_id):
	organization_list = OrganizationUser.objects.filter(id=user_manager_id, state<=2)
	
	return organization_list
#enregion

#region is_user_in_organization
def is_user_in_organization(user_manager_id, organization_list):
	organization_list = OrganizationUser.objects.filter(id=user_manager_id, state<=2)
	return organization_list
#endregion