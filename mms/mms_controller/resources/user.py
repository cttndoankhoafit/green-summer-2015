from mms_backoffice.models import User, OrganizationUser, ActivityUser

from mms_backoffice.resources import UserResource

def is_user_valid(user_id):
	if User.objects.get(id=user_id):
		return True
	return False

def is_user_identify_valid(user_identify):
	if User.objects.get(identify=user_identify):
		return True
	return False

def is_super_administrator(user_id):
	try:
		return User.objects.get(id=user_id).is_superuser	
	except:
		pass
	return False

#region can_get_user
def can_get_user(user_id, accessed_user_id):
	if not is_user_valid(user_id) or not is_user_valid(accessed_user_id):
		return False

	#case 0: if access user is accessed user
	if int(user_id) == int(accessed_user_id):
		return True
	
	#case 1: if access user is super admin
	if is_super_administrator(user_id):
		return True

	return True
	# #case 2: if access user manage at least one oganization that accessed user participate
	# org_usr_list = OrganizationUser.objects.filter(user=user_id, state__lte=2)
	
	# for ou in org_usr_list:
	# 	if OrganizationUser.objects.get(user=accessed_user_id, organization=ou.organization):
	# 		return True

	# #case 3:  if access user manage at least one activity that accessed user participate
	# atv_usr_list = ActivityUser.objects.filter(user=user_id, state__lte=2)
	
	# for au in atv_usr_list:
	# 	if ActivityUser.objects.get(user=accessed_user_id, activity=au.activity):
	# 		return True
	
	# return False
#endregion

#region can_set_user
def can_set_user(user_id_access, user_id_accessed):
	u_access = int(user_id_access)
	u_accessed = int(user_id_accessed)

	if not is_user_valid(u_access) or not is_user_valid(u_accessed):
		return False

	#case 0: if access user is accessed user
	if u_access == u_accessed:
		return True

	user = User.objects.get(id=u_access)
	
	#case 1: if access user is super admin
	if user.is_staff:
		return True

	return False
#endregion

#region get_user
def get_user(user_id_access, user_id_accessed):
	if can_get_user(user_id_access, user_id_accessed):
		return User.objects.get(id=user_id_accessed)
	return None
#endregion

#region set_user
def set_user(user_id_access, user_id_accessed):
	if can_set_user(user_id_access, user_id_accessed):
		return User.objects.get(id=user_id_accessed)
	return None
#endregion

#region can_get_user_list
def can_get_user_list(user_id_access):
	#if user is super admin
	user = User.objects.get(id=user_id_access)
	if user.is_staff:
		return True
	return False
#endregion

#region can_set_user_list
def can_set_user_list(user_id_access):
	#if user is super admin
	user = User.objects.get(id=user_id_access)
	if user.is_staff:
		return True
	return False
#endregion

#region reset_user_password
def reset_user_password(user_id_access, accessed_user_id):
	if can_set_user(user_id_access, accessed_user_id):
		user = User.objects.get(id=accessed_user_id)
		user.set_password(user.identify)
		user.save()
		return user
	return None
#endregion

#region get_user_list
def get_user_list(user_id_access):
	if can_get_user_list(user_id_access):
		return User.objects.all()
	return None
#endregion

#region can_get_managed_user_list
def can_get_managed_user_list(user_id_access):
	#if user manage at least one organization
	org_usr_list = OrganizationUser.objects.filter(user=user_id_access, state__lte=2)
	if len(org_usr_list) > 0:
		return True
	return False
#endregion

#region get_managed_user_list
def get_managed_user_list(user_id_access):
	if can_get_managed_user_list(user_id_access):
		org_list = OrganizationUser.objects.filter(user=user_id_access, state__lte=2).values('organization').distinct()
		return OrganizationUser.objects.filter(organization__in=org_list).values('user').distinct()
	return None
#endregion

def create_user(user_id, user_object):
	if can_set_user_list(user_id):
		if len(user_object.password) > 0:
			user_object.set_password(user_object.password)
		user_object.save()
		return True
	return False

def get_user_resource():
	return UserResource

def get_user_model():
	return User

def create_user_by_infomation(	user_id, 
								identify,
								first_name,
								last_name,
								gender,
								date_of_birth,
								place_of_birth,
								folk,
								religion,
								address,
								ward,
								district,
								province,
								temporary_address,
								home_phone,
								mobile_phone,
								email	):

	if can_set_user_list(user_id):
		try:
			user_object = User(	identify=identify,
							first_name=first_name,
							last_name=last_name,
							gender=gender,
							date_of_birth=date_of_birth,
							place_of_birth=place_of_birth,
							folk=folk,
							religion=religion,
							address=address,
							ward=ward,
							district=district,
							province=province,
							temporary_address=temporary_address,
							home_phone=home_phone,
							mobile_phone=mobile_phone,
							email=email	)

			user_object.set_password(user_object.identify)
			user_object.save()
		except Exception as e:
			print e
			return False

		return True
	return False