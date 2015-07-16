from django.contrib.admin.models import LogEntry
from django.views.generic import ListView

def datetimeToString(dt):
	res = '%d/%d/%d %02d:%02d:%02d' % (dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
	return res

class ActivityLogListView(ListView):
	template_name = 'temporary/member/list.html'

	def get_queryset(self):
		last_log_list = LogEntry.objects.order_by('-action_time')[:10]
		res = []

		for log in last_log_list:
			line = "%s - %s " % (datetimeToString(log.action_time), log.user)

			if log.action_flag == 1:
				line += "added "
			if log.action_flag == 2:
				line += "changed "
			if log.action_flag == 3:
				line += "deleted "

			line += "%s \"%s\"" %(log.content_type, log.object_repr)

			res.append(line)

		return res