from mms_backoffice.models import User

def can_get_user(user_id_access, user_id_accessed):
	user = User.objects.get(id=user_id_access)
	if user.is_staff:
		return True

	return False

def can_set_user(user_id_access, user_id_accessed):
	user = User.objects.get(id=user_id_access)
	if int(user_id_access) == int(user_id_accessed) or user.is_staff:
		return True
	return False

def get_user(user_id_access, user_id_accessed):
	if int(user_id_access) == int(user_id_accessed) or can_get_user(user_id_access, user_id_accessed):
		return User.objects.get(id=user_id_accessed)
	return None

def set_user(user_id_access, user_accessed):
	if user_accessed is None:
		return None
	if can_set_user(user_id_access, user_accessed.id):
		return user_accessed
	return None
