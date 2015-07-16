# -*- coding: utf-8 -*-

from django.utils.html import mark_safe

from django.views.generic import ListView, UpdateView

from mms_backoffice.models import Activity, ActivityUser

class ActivityListView(ListView):
	template_name = 'v1/list.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(ActivityListView, self).get_context_data(**kwargs)

		context['title'] = u'Danh sách hoạt động'
		context['page_title'] = u'Danh sách hoạt động'

		context['activity_active'] = 'active'
		context['activity_list_active'] = 'active'

		context['theads'] = [	{'name': u'Mã số', 'size' : '10%'},
								{'name': u'Tên hoạt động', 'size' : 'auto'},
								{'name': u'Thời gian tổ chức', 'size' : '20%'},
								{'name': u'Trạng thái', 'size' : '20%'},
								{'name': '', 'size' : '8%'},	]

		return context

	def get_color(self, value):
		if value == 0:
			return 'red'
		elif value == 1:
			return 'red-pink'
		elif value == 2:
			return 'red-sunglo'
		elif value == 3:
			return 'yellow'
		elif value == 4:
			return 'purple'
		elif value == 5:
			return 'green'
		elif value == 6:
			return 'blue'

	def get_queryset(self):
		user_list = Activity.objects.all()

		objects = []
		for obj in user_list:
			values = []	
			values.append(obj.id)
			values.append(obj.name)
			values.append(obj.start_time)

			states = ActivityUser.objects.filter(activity=obj.id, user=self.request.session['user_id'])
			state_string = ''
			for s in states:
				state_string += '<div class="margin-bottom-5"><span class="btn label label-sm %s margin-bottom">%s</span></div>' % (self.get_color(s.state), s.get_state_display())
			values.append(mark_safe(state_string))
			values.append(mark_safe(u'<a href="/user/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.id)))
			objects.append(values)

		return objects
class UserActivityListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	def get_queryset(self): 
		identify = self.kwargs['user_id']
		user_activity = ActivityUser.objects.filter(user__id=identify)
		return list(user_activity)