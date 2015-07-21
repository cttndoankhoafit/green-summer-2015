from mms_backoffice.models import Organization, User, OrganizationUser, OrganizationType

from mms_controller.resources.user import *

def is_organization_valid(organization_id):
	try:
		org = Organization.objects.get(id=organization_id)
		return True
	except:
		pass
	return False

def is_organization_identify_valid(organization_identify):
	try:
		org = Organization.objects.get(identify=organization_identify)
		return True
	except:
		pass
	return False

def is_user_in_organization(user_manager_id, organization_list):
	organization_list = OrganizationUser.objects.filter(id=user_manager_id, state__lte=2)
	return organization_list

#region check organization administrator
def check_organization_administrator(user, organization):
	if organization.identify == 'root':
		return False
	try:
		organization_user_object = OrganizationUser.objects.get(user=user, organization=organization, state=0)
		return True
	except:
		pass
	return check_organization_administrator(user, organization.manager_organization)

def is_organization_administrator(user_id, organization_id):
	if not is_user_valid(user_id) or not is_organization_valid(organization_id):
		return False
	if is_super_administrator(user_id):
		return True
	return check_organization_administrator(User.objects.get(id=user_id), Organization.objects.get(id=organization_id))
#endregion


#region check organization manager
def check_organization_manager(user, organization):
	if organization.identify == 'root':
		return False
	try:
		organization_user_object = OrganizationUser.objects.get(user=user, organization=organization, state__lte=2)
		return True
	except:
		pass
	return check_organization_manager(user, organization.manager_organization)

def is_organization_manager(user_id, organization_id):
	if not is_user_valid(user_id) or not is_organization_valid(organization_id):
		return False
	if is_super_administrator(user_id):
		return True
	return check_organization_manager(User.objects.get(id=user_id), Organization.objects.get(id=organization_id))
#endregion


#region can set organization
def can_set_organization(user_id, organization_id):
	if not is_user_valid(user_id) or not is_organization_valid(organization_id):
		return False

	#case 0: if user is super admin
	if is_super_administrator(user_id):
		return True

	#case 1: if user is the administrator of organization
	if is_super_administrator(user_id, organization_id):
		return True

	return False
#endregion


def can_get_organization(user_id_access, organization_id):

	return True


#region can_set_user_list
def can_set_organization_list(user_id):
	#if user is super admin
	if is_super_administrator(user_id):
		return True


	return False
#endregion

#region get organization list
def can_get_organization_list(user_id):

	return True

def get_organization_list(user_id):
	if is_super_administrator(user_id):
		return Organization.objects.all()

	if can_get_organization_list(user_id):
		organization_user_list = OrganizationUser.objects.filter(user=user_id)

		objects = []
		for org_usr in organization_user_list:
			objects.append(org_usr.organization)

		return objects
	return None
#endregion

#region is_user_in_organization

#endregion


def can_manage_organization(user_id):
	if is_super_administrator(user_id):
		return True
		
	#if user is the adminitator at least one organization
	org_usr_list = OrganizationUser.objects.filter(user=user_id, state=0)

	if len(org_usr_list) > 0:
		return True
	return False

#region create_organization
def create_organization(user_manager_id, organization_object):
	if can_manage_organization(user_manager_id):	
		root = get_organization_root()
		if organization_object.manager_organization is None:
			organization_object.manager_organization = root
		organization_object.save()
		return True
	return False

#endregion

def get_organization(user_manager_id, organization_object):
	return Organization.objects.get(id=organization_object)

def get_organization_root():
	organization_object = None
	try:
		organization_object = Organization.objects.get(identify='root')
	except:
		organization_object = Organization(identify='root')
		organization_object.save()
	return organization_object

def create_organization_by_infomation(user_manager_id, identify, name, organization_type):
	if can_manage_organization(user_manager_id):
		root = get_organization_root()
		try:
			organization_object = Organization(	identify=identify,
												name=name,
												manager_organization=root,
												organization_type=OrganizationType.objects.get(identify=organization_type)	)
			organization_object.save()
			organization_user_object = OrganizationUser( 	organization=organization_object,
															user=User.objects.get(id=user_manager_id),
															state=0	)
			organization_user_object.save()
		except Exception as e:
			print e
			return False


#region create organization management by information
def create_organization_managerment_by_infomation(user_id, manager_organization_identify, managed_organization_identify):
	try:
		if can_set_organization(user_id, manager_organization_identify) and can_set_organization(user_id, managed_organization_identify):
			manager = Organization.objects.get(identify=manager_organization_identify)
			managed = Organization.objects.get(identify=managed_organization_identify)

			if (manager.organization_type.management_level < managed.organization_type.management_level):
				managed.manager_organization = manager
				managed.save()

	except Exception as e:
		print e
		return False
#endregion

#region Add organization user by identify
def can_add_organization_user(manager_id, organization_id, user_id):
	if not is_user_valid(manager_id) or not is_user_valid(user_id) or not is_organization_valid(organization_id):
		return False

	if is_organization_administrator(manager_id, organization_id):
		return True

	return False

def add_organization_user(manager_id, organization_id, user_id, state=3):
	if is_super_administrator(user_id):
		return
	if can_add_organization_user(manager_id, organization_id, user_id):
		organization_user_object = OrganizationUser(organization=organization_id, user=user_id, state=state)
		organization_user_object.save()
#endregion

#region Add organization user by identify code
def can_add_organization_user_by_identify(manager_id, organization_identify, user_identify):
	if not is_user_valid(manager_id) or not is_user_identify_valid(user_identify) or not is_organization_identify_valid(organization_identify):
		return False

	organization_id = Organization.objects.get(identify=organization_identify).id
	if is_organization_administrator(manager_id, organization_id):
		return True

	return False

def add_organization_user_by_identify(manager_id, organization_identify, user_identify, state=3):
	if can_add_organization_user_by_identify(manager_id, organization_identify, user_identify):
		user_id = User.objects.get(identify=user_identify).id
		if is_super_administrator(user_id):
			return
			
		organization_id = Organization.objects.get(identify=organization_identify)
		user_id = User.objects.get(identify=user_identify)

		organization_user_object = OrganizationUser(organization=organization_id, user=user_id, state=state)
		organization_user_object.save()
#endregion


#region Set organization user
def can_set_organization_user(manager_id, organization_id, user_id):
	if not is_user_valid(manager_id) or not is_user_valid(user_id) or not is_organization_valid(organization_id):
		return False

	if is_organization_administrator(manager_id, organization_id):
		return True

	return False

def set_organization_user(manager_id, organization_id, user_id):
	if not is_user_valid(manager_id) or not is_user_valid(user_id) or not is_organization_valid(organization_id):
		return None

	if is_organization_administrator(manager_id, organization_id):
		try:
			return OrganizationUser.objects.get(organization=organization_id, user=user_id)
		except:
			pass

	return None
#endregion

#region get organizaton user list
def get_under_organization_list(organization):
	organization_list = Organization.objects.filter(manager_organization=organization)

	objects = []
	objects.append(organization)
	for obj in organization_list:
		objects += get_under_organization_list(obj)

	return objects

def get_organization_user_list(user_id, organization_id):
	if is_organization_manager(user_id, organization_id):
		organization_user_list = OrganizationUser.objects.filter(organization__in=get_under_organization_list(Organization.objects.get(id=organization_id)))

		objects = []
		for org_usr in organization_user_list:
			objects.append(org_usr.user)

		return objects
	return None
#endregion

#region get organization tuple table
def get_organization_tuple_table(user_id, organization):
	organization_list = Organization.objects.filter(manager_organization=organization)

	objects = []
	for obj in organization_list:
		objects.append(get_organization_tuple_table(user_id, obj))

	return (organization, objects)

def get_organization_tuple_table_by_id(user_id, organization_id):
	organization = Organization.objects.get(id=organization_id)
	return get_organization_tuple_table(user_id, organization_id)
#endregion