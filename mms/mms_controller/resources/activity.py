from mms_backoffice.models import Activity, User

def get_activity_user_list(user_id, activity_id):
	return ActivityUser.objects.filter(id=activity_id)

def get_activity_list(user_id):
	return Activity.objects.all()

def get_activity_model():
	return Activity

