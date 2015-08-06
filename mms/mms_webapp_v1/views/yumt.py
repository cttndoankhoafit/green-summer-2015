# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.utils.html import mark_safe

from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, FormView

from django.http import HttpResponseRedirect, HttpResponse, Http404

from django.core.urlresolvers import reverse_lazy, reverse

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_webapp_v1.views.bases.base_view import *

from mms_base.resources import *


class BaseYUMTView(BaseView):

	def get_context_data(self, **kwargs):
		context = super(BaseYUMTView, self).get_context_data(**kwargs)

		context['yumt_active'] = 'active'
		
		return context



class YUMTListView(BaseYUMTView, ListView):
	template_name = 'v1/static_pages/list.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(YUMTListView, self).get_context_data(**kwargs)

		context['theads'] = [	{'name': u'Năm học', 'size' : 'auto'},	
								{'name': u'Xếp loại', 'size' : '15%'}	]
		return context

	def get_queryset(self):
		yumt_list = get_yumt_list()

		objects = []
 		for obj in yumt_list:
 			values = []
 			values.append(obj)
 			values.append('')
 			objects.append(values)
		return objects



class YUMTRegisterView(BaseYUMTView, ListView, FormView):
	template_name = 'v1/yumt/register.html'
	
	def get_context_data(self, **kwargs):
		context = super(YUMTRegisterView, self).get_context_data(**kwargs)

		context['theads'] = [	{'name': u'#', 'size' : '10%'},	
								{'name': u'Tên hoạt động', 'size' : 'auto'},
								{'name': u'Loại rèn luyện', 'size' : '15%'},
								{'name': u'Thời gian', 'size' : '15%'}	]

		context['show_checkbox'] = 1

		return context

	def get_success_url(self):
		return reverse('yumt_register_view_v1')

	def get_queryset(self):
		activity_list = get_activity_list()
		for obj in activity_list:
			if is_registered_yumt_activity(self.get_user_id(), obj.identify):
				obj.registered = 1
			else:
				obj.registered = 0
			if obj.training_type == 0:
				obj.type = 0
			elif obj.training_type == 1:
				obj.type = 1
			else:
				obj.type = 2

		return activity_list

	def post(self, request, *args, **kwargs):
		if 'list' in request.POST:
			activity_list = request.POST.getlist('list')
			submit_list = request.POST.getlist('submit')
			print submit_list
			if u'Đăng ký' in submit_list:
				for obj in activity_list:
					register_yumt_activity(self.get_user_id(), obj)
			elif u'Hủy Đăng ký' in submit_list:
				for obj in activity_list:
					unregister_yumt_activity(self.get_user_id(), obj)
		return self.get(self, *args, **kwargs)



class YUMTFormView(FormView):
	def get_context_data(self, **kwargs):
		if not is_super_administrator(self.get_user_id()):
			raise PermissionDenied

		context = super(YUMTFormView, self).get_context_data(**kwargs)

		return context

	def get_form(self, form_class):
		form = super(YUMTFormView, self).get_form(form_class)
		
		form.fields['register_start_time'].widget.attrs['class'] = 'form-control'
		form.fields['register_start_time'].widget.attrs['readonly'] = '1'

		form.fields['register_end_time'].widget.attrs['class'] = 'form-control'
		form.fields['register_end_time'].widget.attrs['readonly'] = '1'
		
		form.fields['judge_start_time'].widget.attrs['class'] = 'form-control'
		form.fields['judge_start_time'].widget.attrs['readonly'] = '1'

		form.fields['judge_end_time'].widget.attrs['class'] = 'form-control'
		form.fields['judge_end_time'].widget.attrs['readonly'] = '1'

		return form



class YUMTCreateView(BaseYUMTView, CreateView, YUMTFormView):
	template_name = 'v1/yumt/editor/creator.html'

	model = get_yumt_model()

	fields = [	'period',
				'register_start_time',
				'register_end_time',
				'judge_start_time',
				'judge_end_time' ]

	success_message = u''

	# def get_success_url(self):
	# 	return reverse('user_password_change_view_v1', kwargs={'user_id' : self.get_user_account_id() })

	def get_context_data(self, **kwargs):
		context = super(YUMTCreateView, self).get_context_data(**kwargs)

		context['page_title'] = u'Tạo chương trình rèn luyện Đoàn viên'

		context['button_value'] = u'Tạo chương trình'

		return context

	def get_form(self, form_class):
		form = super(YUMTCreateView, self).get_form(form_class)
		form.fields['period'].widget.attrs['class'] = 'form-control'
		return form

	def form_valid(self, form):
		self.object = form.save(commit=False)
		
		set_yumt(self.get_user_id(), self.object)
			
		# self.clear_messages()

		return super(YUMTCreateView, self).form_valid(form)


class YUMTUpdateView(BaseYUMTView, UpdateView, YUMTFormView):
	template_name = 'v1/yumt/editor/creator.html'

	fields = [	'register_start_time',
				'register_end_time',
				'judge_start_time',
				'judge_end_time' ]

	def get_period_id(self):
		return self.kwargs['period_id']

	def get_context_data(self, **kwargs):
		context = super(YUMTUpdateView, self).get_context_data(**kwargs)

		context['page_title'] = u'Cập nhật chương trình'

		context['button_value'] = u'Cập nhật'

		return context


	def form_valid(self, form):
		self.object = form.save(commit=False)
		
		set_yumt(self.get_user_id(), self.object)
			
		# self.clear_messages()

		return super(YUMTUpdateView, self).form_valid(form)


	def get_object(self):
		return get_yumt(self.get_period_id())