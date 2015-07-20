# -*- coding: utf-8 -*-

from django.utils.html import mark_safe

from django.views.generic import ListView, UpdateView, TemplateView

from mms_backoffice.models import Activity, ActivityUser, ActivityOrganization

class ActivityUpdateView(TemplateView):
	template_name = 'v1/activity/lish.html'

class ActivityListView(ListView):
	# template v1/activity/list.html cần anh sửa, 
	# hiện h em đang chạy template v1/list.html
	# template_name = 'v1/activity/list.html'
	template_name = 'v1/list.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(ActivityListView, self).get_context_data(**kwargs)

		context['title'] = u'Danh sách hoạt động'
		context['page_title'] = u'Danh sách hoạt động'

		context['user_active'] = 'active'
		context['user_list_active'] = 'active'

		context['theads'] = [	{'name': u'Tên hoạt động', 'size' : 'auto'},
								{'name': u'Tổ chức', 'size' : 'auto'},
								{'name': u'Loại', 'size' : 'auto'},
								{'name': u'Bắt đầu', 'size' : 'auto'},
								{'name': u'Kết thúc', 'size' : 'auto'},
								{'name': u'Mô tả', 'size' : 'auto'}
							]

		return context

	def get_color(self, value):
		if value == 0:
			return 'blue'
		elif value == 1:
			return 'green'
		elif value == 2:
			return 'purple'

	def get_queryset(self):
		user_list = Activity.objects.all()

		objects = []
		for obj in user_list:
			values = []
			#Tên hoạt động
			values.append(obj.name)
			#Đơn vị tổ chức
			org = ActivityOrganization.objects.filter(activity=obj.id)
			state_string = ''
			for s in org:
				state_string += s.organization.name
			values.append(mark_safe(state_string))
			#Loại hoạt động
			org = ActivityOrganization.objects.filter(activity=obj.id)
			state_string = ''
			state_string += '<div class="margin-bottom-5"><span class="btn label label-sm %s margin-bottom">%s</span></div>' % (self.get_color(obj.activity_type), obj.get_activity_type_display())
			values.append(mark_safe(state_string))
			#Thời gian bắt đầu - kết thúc
			values.append(obj.start_time)
			values.append(obj.end_time)
			#Mô tả hoạt động
			values.append(obj.details)
			objects.append(values)

		return objects

class UserActivityListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	def get_queryset(self): 
		identify = self.kwargs['user_id']
		user_activity = ActivityUser.objects.filter(user__id=identify)
		return list(user_activity)