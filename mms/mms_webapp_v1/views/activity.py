# -*- coding: utf-8 -*-

from django.utils.html import mark_safe

from django.views.generic import ListView, UpdateView

class ActivityListView(ListView):
	template_name = 'v1/list.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(ActivityListView, self).get_context_data(**kwargs)

		context['title'] = u'Danh sách hoạt động'
		context['page_title'] = u'Danh sách hoạt động'

		context['activity_active'] = 'active'
		context['activity_list_active'] = 'active'

		context['theads'] = [	{'name': u'Mã hoạt động', 'size' : '20%'},
								{'name': u'Tên hoạt động', 'size' : 'auto'},
								{'name': u'Thời gian tổ chức', 'size' : '20%'},
								{'name': u'Trạng thái', 'size' : '20%'},	]

		return context

	def get_queryset(self):
		# user_list = User.objects.all()

		objects = []
		# for obj in user_list:
		# 	values = []	
		# 	values.append(obj.identify)
		# 	values.append(obj.get_full_name())
		# 	values.append(mark_safe(u'<a href="/user/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.id)))
		# 	objects.append(values)

		return objects