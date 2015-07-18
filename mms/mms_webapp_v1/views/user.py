# -*- coding: utf-8 -*-

from django.utils.html import mark_safe

from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DetailView

from mms_backoffice.models import User

from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse_lazy, reverse

from mms_controller.resources.user import *

# from django.shortcuts import render

class MemberListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	def get_queryset(self):
		return None

success_update_string = u'Cập nhật thông tin thành công'
# def SucessFullUpdateUser(request):
# 	template_name = 'v1/user/edit.html'
# 	context = { 'message': u'Cập nhật thông tin thành công' }
# 	return render(request, template_name, context)


class UserDetailView(DetailView):
	model = User
	template_name = 'v1/user/user_profile.html'

	def get_context_data(self, **kwargs):
		context = super(UserDetailView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['user_active'] = 'active'
		context['profile_active'] = 'active'

		context['page_breadcrumb'] = mark_safe(u'<li><i class="fa fa-user"></i><a>Quản lý tài khoản</a><i class="fa fa-angle-right"></i></li><li><i class="fa fa-user"></i><a>Thông tin cá nhân</a></li>')
		return context

	def get_object(self):
		return get_user(	self.request.session['user_id'],
							self.kwargs['user_id']
						)

class UserProfileView(UserDetailView):
	model = User
	template_name = 'v1/user/user_profile.html'

	def get_context_data(self, **kwargs):
		context = super(UserDetailView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['user_active'] = 'active'
		context['profile_active'] = 'active'

		context['page_breadcrumb'] = mark_safe(u'<li><i class="fa fa-user"></i><a>Quản lý tài khoản</a><i class="fa fa-angle-right"></i></li><li><i class="fa fa-user"></i><a>Thông tin cá nhân</a></li>')
		return context

	def get_object(self):
		return get_user(	self.request.session['user_id'],
							self.request.session['user_id']
						)
		
class UserUpdateView(UpdateView):
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

	template_name = 'v1/user/user_update.html'

	def get_form(self, form_class):
		form = super(UpdateView, self).get_form(form_class)
		form.fields['first_name'].widget.attrs['class'] = 'form-control'
		form.fields['last_name'].widget.attrs['class'] = 'form-control'
		form.fields['gender'].widget.attrs['class'] = 'form-control'
		form.fields['date_of_birth'].widget.attrs['class'] = 'form-control'
		form.fields['date_of_birth'].widget.attrs['readonly'] = '1'
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

	def get_context_data(self, **kwargs):
		context = super(UserUpdateView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['user_active'] = 'active'

		context['member_full_name'] = self.object.get_full_name()

		return context

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.creator = self.request.user
		self.object.status = 0
		# self.request.session['user'] = self.object

		user_id = self.request.session['user_id']
		user = self.kwargs['user_id']

		if int(user) == user_id:
			self.request.session['user_full_name'] = self.object.get_full_name()
		
		self.object.save()
		return HttpResponseRedirect(reverse('user_update_view_v1', kwargs={'user_id' : user }))

	def get_object(self):
		return set_user(	self.request.session['user_id'],
							get_user(	self.request.session['user_id'], 
										self.kwargs['user_id']
									)
						)

class UserProfileUpdateView(UserUpdateView):

	template_name = 'v1/user/edit_profile.html'

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.creator = self.request.user
		self.object.status = 0
		
		self.request.session['user_full_name'] = self.object.get_full_name()
		
		self.object.save()
		return HttpResponseRedirect(reverse('user_profile_update_view_v1'))


	def get_object(self):
		return set_user(	self.request.session['user_id'],
							get_user(	self.request.session['user_id'], 
										self.request.session['user_id']
									)
						)

class UserResetPasswordView(DetailView):
	template_name = 'v1/user/reset_password.html'
	
	def get_context_data(self, **kwargs):
		context = super(UserResetPasswordView, self).get_context_data(**kwargs)

		return context

	def get_object(self):
		return User.objects.get(id=self.kwargs['user_id'])

class UserResetPasswordDoneView(DetailView):
	template_name = 'v1/user/reset_password_done.html'
	
	def get_context_data(self, **kwargs):
		context = super(UserResetPasswordDoneView, self).get_context_data(**kwargs)

		return context

	def get_object(self):
		user = User.objects.get(id=self.kwargs['user_id'])
		user.password = None
		user.save()
		return user

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
		user_list = None
		user = User.objects.get(id=self.request.session['user_id'])
		if user.is_staff:
			user_list = User.objects.order_by('identify')

		objects = []
		if user_list is not None:
			for obj in user_list:
				values = []	
				values.append(obj.identify)
				values.append(obj.get_full_name())
				values.append(mark_safe(u'<a href="/user/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.id)))
				objects.append(values)

		return objects

class UserCreateView(CreateView):
	model = User
	fields =[	'identify',
				'first_name',
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

	template_name = 'v1/user/create.html'

 	def get_form(self, form_class):
		form = super(UserCreateView, self).get_form(form_class)
		return form

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.save()
		return HttpResponse('Create User success')

	def form_invalid(self, form):
		return HttpResponse("Failed")
