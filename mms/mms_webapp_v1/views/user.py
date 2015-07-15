# -*- coding: utf-8 -*-

from django.views.generic import ListView, TemplateView, UpdateView

from mms_backoffice.models import User

class MemberListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	def get_queryset(self):
		return None

class UserFormView:
	def get_form(self, form_class):
		form = super(UserProfileView, self).get_form(form_class)
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

class UserProfileView(UserFormView, UpdateView):
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
	
	def get_context_data(self, **kwargs):
		context = super(UserProfileView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['member_name'] = self.objects.get_full_name()
		context['member_full_name'] = self.objects.get_full_name()

		return context

	

	def get_object(self):
		return User.objects.get(id=self.request.session['user_id'])

class UserUpdateView(UserFormView, UpdateView):
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
	
	def get_context_data(self, **kwargs):
		context = super(UserUpdateView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['member_name'] = self.objects.get_full_name()
		context['member_full_name'] = self.objects.get_full_name()

		return context
		
	def get_object(self):
		return User.objects.get(identify=self.kwargs['user_identify'])


class UserListView(TemplateView):
	template_name = 'v1/list.html'

	def get_context_data(self, **kwargs):
		context = super(UserListView, self).get_context_data(**kwargs)

		context['title'] = u'Quản lý tài khoản'
		context['page_title'] = u'Quản lý tài khoản'
		context['user_active'] = u'active'
		
		context['member_name'] = User.objects.get(id = self.request.session['user_id']).get_full_name()

		return context