from mms_backoffice.models import Organization, User, OrganizationUser

#region can_get_organization
def can_get_organization(user_id_access, organization_id):
	# if not is_user_valid(user_id_access) or not is_user_valid(user_id_accessed):
	# 	return False

	# #case 0: if access user is accessed user
	# if int(user_id_access) == int(user_id_accessed):
	# 	return True
	
	# #case 1: if access user is super admin
	# if user.is_staff:
	# 	return True

	# #case 2: if access user manage at least one oganization that accessed user participate
	# org_usr_list = OrganizationUser.objects.filter(user=user_id_access, state__lte=2)
	
	# for ou in org_usr_list:
	# 	if OrganizationUser.objects.get(user=user_id_accessed, organization=ou.organization):
	# 		return True

	# #case 3:  if access user manage at least one activity that accessed user participate
	# atv_usr_list = ActivityUser.objects.filter(user=user_id_access, state__lte=2)
	
	# for au in atv_usr_list:
	# 	if ActivityUser.objects.get(user=user_id_accessed, activity=au.activity):
	# 		return True
	
	return True
#endregion

#region can_set_organization
def can_set_organization(user_id_access, organization_id):
	# if not is_user_valid(user_id_access) or not is_user_valid(user_id_accessed):
	# 	return False

	# #case 0: if access user is accessed user
	# if int(user_id_access) == int(user_id_accessed):
	# 	return True

	# user = User.objects.get(id=user_id_access)
	
	# #case 1: if access user is super admin
	# if user.is_staff:
	# 	return True

	return True
#endregion

#region can_get_organization_list
def can_get_organization_list(user_id_access):
	#if user is super admin
	user = User.objects.get(id=user_id_access)
	if user.is_staff:
		return True
	return False
#endregion

#region can_set_user_list
def can_set_organization_list(user_id_access):
	#if user is super admin
	user = User.objects.get(id=user_id_access)
	if user.is_staff:
		return True
	return False
#endregion

#region get_organization_list
def get_organization_list(user_id_access):
	if can_get_organization_list(user_id_access):
		return Organization.objects.all()
	return None
#endregion

#region can_get_managed_organization_list
def can_get_managed_organization_list(user_id_access):
	#if user manage at least one organization
	org_usr_list = OrganizationUser.objects.filter(user=user_id_access, state__lte=2)
	if len(org_usr_list) > 0:
		return True
	return False
#endregion

#region get_organization_user_manage
def get_managed_organization_list(user_manager_id):
	if can_get_managed_organization_list(user_manager_id):
		organization_list = OrganizationUser.objects.filter(id=user_manager_id, state__lte=2).values('organization').distinct()	
	return None
#enregion

#region is_user_in_organization
def is_user_in_organization(user_manager_id, organization_list):
	organization_list = OrganizationUser.objects.filter(id=user_manager_id, state__lte=2)
	return organization_list
#endregion


def can_create_organization(user_manager_id):
	user = User.objects.get(id=user_manager_id)
	if user.is_staff:
		return True
		
	#if user is the adminitator at least one organization
	org_usr_list = OrganizationUser.objects.filter(user=user_manager_id, state=0)
	if len(org_usr_list) > 0:
		return True
	return False

#region create_organization
def create_organization(user_manager_id, organization_object):
	if can_create_organization(user_manager_id):	
		root = None
		if Organization.objects.count() == 0:
			root = Organization(name='root')
			root.save()
		else:
			root = Organization.objects.get(name='root')

		if organization_object.organization_manager is None:
			organization_object.organization_manager = root
		organization_object.save()
		return True
	return False

#endregion

def get_organization(user_manager_id, organization_object):
	return Organization.objects.get(id=organization_object)