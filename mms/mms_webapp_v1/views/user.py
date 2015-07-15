# -*- coding: utf-8 -*-

from django.utils.html import mark_safe

from django.views.generic import ListView, TemplateView, UpdateView

from mms_backoffice.models import User

class MemberListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	def get_queryset(self):
		return None

class UserFormView(UpdateView):
	model = User

	fields =[	'first_name',
				'last_name',
				'gender',
				'date_of_birth',
				'place_of_birth',
				'folk',
				'religion',
				'address',
				'ward',
				'district',
				'province',
				'temporary_address',
				'home_phone',
				'mobile_phone',
				'email' ]

	template_name = 'v1/user/profile.html'

	def get_form(self, form_class):
		form = super(UserFormView, self).get_form(form_class)
		form.fields['first_name'].widget.attrs['class'] = 'form-control'
		form.fields['last_name'].widget.attrs['class'] = 'form-control'
		form.fields['gender'].widget.attrs['class'] = 'form-control'
		form.fields['date_of_birth'].widget.attrs['class'] = 'form-control input-sm form-filter'
		# form.fields['date_of_birth'].widget.attrs['readonly']
		form.fields['place_of_birth'].widget.attrs['class'] = 'form-control'
		form.fields['folk'].widget.attrs['class'] = 'form-control'
		form.fields['religion'].widget.attrs['class'] = 'form-control'
		form.fields['address'].widget.attrs['class'] = 'form-control'
		form.fields['ward'].widget.attrs['class'] = 'form-control'
		form.fields['district'].widget.attrs['class'] = 'form-control'
		form.fields['province'].widget.attrs['class'] = 'form-control'
		form.fields['temporary_address'].widget.attrs['class'] = 'form-control'
		form.fields['home_phone'].widget.attrs['class'] = 'form-control'
		form.fields['mobile_phone'].widget.attrs['class'] = 'form-control'
		form.fields['email'].widget.attrs['class'] = 'form-control'

		return form

class UserProfileView(UserFormView):
	
	def get_context_data(self, **kwargs):
		context = super(UserProfileView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['user_active'] = 'active'
		context['profile_active'] = 'active'

		context['member_full_name'] = self.object.get_full_name()

		return context

	def get_object(self):
		return User.objects.get(id=self.request.session['user_id'])

class UserUpdateView(UserFormView):
	def get_context_data(self, **kwargs):
		context = super(UserUpdateView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['user_active'] = 'active'

		context['member_full_name'] = self.object.get_full_name()

		return context

	def get_object(self):
		return User.objects.get(id=self.kwargs['user_id'])


class UserListView(ListView):
	template_name = 'v1/list.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(UserListView, self).get_context_data(**kwargs)

		context['title'] = u'Danh sách tài khoản'
		context['page_title'] = u'Danh sách tài khoản'

		context['user_active'] = 'active'
		context['user_list_active'] = 'active'

		context['theads'] = [	{'name': u'Mã số', 'size' : '20%'},
								{'name': u'Họ và Tên', 'size' : 'auto'},
								{'name': '', 'size' : '8%'},	]

		return context

	def get_queryset(self):
		user_list = User.objects.all()

		objects = []
		for obj in user_list:
			values = []	
			values.append(obj.identify)
			values.append(obj.get_full_name())
			values.append(mark_safe(u'<a href="/user/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.id)))
			objects.append(values)

		return objects
