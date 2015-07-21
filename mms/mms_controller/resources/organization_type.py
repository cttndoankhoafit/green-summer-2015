from mms_backoffice.models import OrganizationType, User

def can_set_organization_type(user_id):
	try:
		user = User.objects.get(id=user_id)
		return user.is_staff
	except:
		pass
	return None

def can_create_organization_type(user_id):
	try:
		user = User.objects.get(id=user_id)
		return user.is_staff
	except:
		pass
	return None

def create_organization_type_by_infomation(user_id, identify, name, management_level):
	if can_create_organization_type(user_id):
		try:
			organization_type_object = OrganizationType(identify=identify, name=name, management_level=management_level)
			organization_type_object.save()
		except:
			pass

def get_organization_type_list():
	return OrganizationType.objects.all()

def get_organization_type_model():
	return OrganizationType