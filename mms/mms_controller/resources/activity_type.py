from mms_backoffice.models import ActivityType

from mms_controller.resources.user import *

def can_set_activity_type(user_id):
	return is_super_administrator(user_id)

def can_create_activity_type(user_id):
	return is_super_administrator(user_id)

def create_activity_type_by_infomation(user_id, identify, name):
	if can_create_activity_type(user_id):
		try:
			activity_type_object = ActivityType(identify=identify, name=name)
			activity_type_object.save()
		except:
			pass

def get_activity_type_list():
	return ActivityType.objects.all()
