# -*- coding: utf-8 -*-

from django.utils.html import mark_safe

from django.views.generic import ListView, UpdateView, TemplateView, DetailView

from mms_backoffice.models import Activity, ActivityUser, ActivityOrganization

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_controller.resources.activity import *

class ActivityListView(ListView):
	template_name = 'v1/list.html'
	paginate_by = '20'

	can_set = True

	def get_context_data(self, **kwargs):
		context = super(ActivityListView, self).get_context_data(**kwargs)

		context['title'] = u'Danh sách hoạt động'
		context['page_title'] = u'Danh sách hoạt động'

		context['user_active'] = 'active'
		context['user_list_active'] = 'active'

		context['theads'] = [	{'name': u'Tên hoạt động', 'size' : 'auto'},
								{'name': u'Loại hoạt động', 'size' : '15%'},
								{'name': u'Thời gian tổ chức', 'size' : '15%'},
								# {'name': u'Trạng thái', 'size' : 'auto'},
								{'name': u'', 'size' : '15%'},
							]

		if self.can_set:
			context['can_set_list'] = 1

		return context

	def get_color(self, value):
		if value == 0:
			return 'blue'
		elif value == 1:
			return 'green'
		elif value == 2:
			return 'purple'

	def get_queryset(self):
		activity_list = get_activity_list(self.request.session['user_id'])

		objects = []
		for obj in activity_list:
			values = []
			if self.can_set:
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="1" id="%s"/>' % obj.id))
			values.append(obj.name)
			values.append(obj.activity_type)
			values.append(obj.start_time)
			buttons = ''
			if obj.register_state < 3:
				buttons += u'<a class="btn default btn-xs green-stripe">Đăng ký</a>'
			buttons += u'<a href="/user/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % obj.id
			values.append(mark_safe(buttons))

			objects.append(values)
		return objects

class UserActivityListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	

	def get_queryset(self): 
		identify = self.kwargs['user_id']
		user_activity = ActivityUser.objects.filter(user__id=identify)
		return list(user_activity)

class ActivityDetailView(DetailView):
	template_name = 'v1/activity/activity_overview.html'


class ActivityMemberListView(ListView):
	template_name = 'v1/activity/activity_member.html'
	paginate_by = '20'

class ActivityImportView(BaseImportView):
	template_name = 'v1/import.html'

	# CONST_FIELDS = (	'identify',
	# 					'name',
	# 					'organization_type'	)

	# def get_success_url(self):
	# 	return reverse('organization_tree_view_v1')

	# def input_row(self, row):
	# 	try:
	# 		for field in self.CONST_FIELDS:
	# 			print row[field]
	# 	except Exception as e:
	# 		return e
		
	# 	identify = row['identify']
	# 	name = row['name']
	# 	organization_type = row['organization_type']

	# 	create_organization_by_infomation(	self.request.session['user_id'],
	# 										identify,
	# 										name,
	# 										organization_type	)

	# 	print '-------------'
	# 	return 'ok'