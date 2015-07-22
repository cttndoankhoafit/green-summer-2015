# -*- coding: utf-8 -*-


from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.utils.html import mark_safe
from django.views.generic import ListView, UpdateView, CreateView, DetailView, View, FormView

from django.contrib.auth.forms import PasswordChangeForm

from django.template.response import TemplateResponse

from mms_controller.resources.user import *
from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

success_create_user_message = u'Thêm người dùng thành công'
success_update_user_message = u'Cập nhật thông tin thành công'
success_reset_password_message = u'Đặt lại mật khẩu thành công'

class UserDetailView(DetailView):
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
		try:
			return get_user(	self.request.session['user_id'],
							self.kwargs['user_id']
						)

		except:
			raise Http404("User is not exist!")


class UserProfileView(UserDetailView):
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
		try:
			return get_user(	self.request.session['user_id'],
							self.request.session['user_id']
						)

		except:
			raise Http404("User does not exist!")
		
class UserFormView(BaseSuccessMessageMixin, FormView):
	def get_form(self, form_class):
		form = super(UserFormView, self).get_form(form_class)
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

class BaseUserUpdateView(UpdateView, UserFormView):
	model = get_user_model()

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
	
	success_message = success_update_user_message

	def get_context_data(self, **kwargs):
		context = super(BaseUserUpdateView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['user_active'] = 'active'

		context['member_full_name'] = self.object.get_full_name()

		return context

class UserUpdateView(BaseUserUpdateView):
	template_name = 'v1/user/user_update.html'

	def get_success_url(self):
		return reverse('user_update_view_v1', kwargs={'user_id' : self.kwargs['user_id'] })

	def form_valid(self,form):
		self.object = form.save(commit=False)
		self.object.creator = self.request.user
		self.object.status = 0

		user_id = self.request.session['user_id']
		user = self.kwargs['user_id']

		if int(user) == user_id:
			self.request.session['user_full_name'] = self.object.get_full_name()
		
		self.object.save()

		self.clear_messages()

		return super(UserUpdateView, self).form_valid(form)

	def get_object(self):
		try:
			return set_user(	self.request.session['user_id'],
							self.kwargs['user_id']
						)

		except:
			raise Http404('User does not exist!')

class UserProfileUpdateView(BaseUserUpdateView):
	template_name = 'v1/user/user_edit_profile.html'

	def get_success_url(self):
		return reverse('user_profile_update_view_v1')

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.creator = self.request.user
		self.object.status = 0
		
		self.request.session['user_full_name'] = self.object.get_full_name()
		
		self.object.save()

		return super(UserProfileUpdateView, self).form_valid(form)

	def get_object(self):
		try:
			return set_user(	self.request.session['user_id'],
							self.request.session['user_id']
						)
		except:
			raise Http404('User does not exist')

class UserResetPasswordView(BaseSuccessMessageMixin, UpdateView):
	template_name = 'v1/user/user_reset_password.html'
	success_message = success_reset_password_message

	fields = []

	def get_context_data(self, **kwargs):
		context = super(UserResetPasswordView, self).get_context_data(**kwargs)

		return context

	def get_success_url(self):
		return reverse('user_reset_password_view_v1', kwargs={'user_id' : self.kwargs['user_id'] })

	def form_valid(self, form):
		
		self.clear_messages()

		return super(UserResetPasswordView, self).form_valid(form)

	def get_object(self):
		try:
			return reset_user_password(self.request.session['user_id'], self.kwargs['user_id'])
		except:
			raise Http404('User does not exist!')

class UserPasswordChangeView(BaseSuccessMessageMixin, FormView):
	template_name = 'v1/user/user_change_password.html'
	form_class = PasswordChangeForm
	success_message = success_reset_password_message

	def get_success_url(self):
		return reverse('user_password_change_view_v1')

	def get_form_kwargs(self):
		kwargs = super(UserPasswordChangeView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form.save()

		self.clear_messages()

		return super(UserPasswordChangeView, self).form_valid(form)

class UserCreateView(CreateView, UserFormView):
	model = get_user_model()

	fields =[	'identify',
				'password',
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

	template_name = 'v1/user/user_create.html'

	success_message = success_create_user_message

	def get_success_url(self):
		return reverse('user_list_view_v1')

 	def get_form(self, form_class):
		form = super(UserCreateView, self).get_form(form_class)
		form.fields['identify'].widget.attrs['class'] = 'form-control'
		form.fields['password'].widget.attrs['class'] = 'form-control'
		return form

	def form_valid(self, form):
		self.object = form.save(commit=False)
		
		if create_user(self.request.session['user_id'], self.object):
			self.clear_messages()
			return super(UserCreateView, self).form_valid(form)

class UserListView(ListView, FormView):
	template_name = 'v1/list.html'
	paginate_by = '20'

	can_set = False
	
	def get_context_data(self, **kwargs):
		context = super(UserListView, self).get_context_data(**kwargs)

		context['title'] = u'Danh sách tài khoản'
		context['page_title'] = u'Danh sách tài khoản'

		context['user_active'] = 'active'
		context['user_list_active'] = 'active'

		context['theads'] = [	{'name': u'Mã số', 'size' : '20%'},
								{'name': u'Họ và Tên', 'size' : 'auto'},
								{'name': '', 'size' : '8%'},	]

		context['add_link'] = '/user/create/'
		context['import_link'] = '/user/import/'

		if self.can_set:
			context['can_set_list'] = 1

		return context

	def get_queryset(self):
		
		user_list =None

		self.can_set = can_set_user_list(self.request.session['user_id'])
		
		can_get = can_get_user_list(self.request.session['user_id'])

		can_get_managed_user = can_get_managed_user_list(self.request.session['user_id'])

		
		if can_get:
			user_list = get_user_list(self.request.session['user_id'])
		else:
			if can_get_managed_user:
				user_list = get_managed_user_list(self.request.session['user_id'])
	

		objects = []
		if user_list is not None:
			for obj in user_list:
				values = []	
				if self.can_set:
					values.append(mark_safe('<input type="checkbox" class="checkboxes" value="%s" name="list"/>' % obj.id))
				values.append(obj.identify)
				values.append(obj.get_full_name())
				values.append(mark_safe(u'<a href="/user/%s" class="btn default btn-xs green-stripe">Chi tiết</a>' % (obj.id)))
				objects.append(values)

		return objects

	def post(self, request, *args, **kwargs):
		print request.POST
		if 'list' in request.POST:
			todel = request.POST.getlist('list')
			print todel
		return self.get(self, *args, **kwargs) #HttpResponseRedirect(reverse('user_list_view_v1'))

#region ImportView
class UserImportView(BaseImportView):
	template_name = 'v1/import.html'

	CONST_FIELDS = (	'identify',
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
						'email'	)

	def get_success_url(self):
		return reverse('user_list_view_v1')

	def input_row(self, row):
		try:
			for field in self.CONST_FIELDS:
				print row[field]
		except Exception as e:
			return e
		
		identify = row['identify']
		first_name = row['first_name']
		last_name = row['last_name']
		gender = row['gender']
		date_of_birth = row['date_of_birth']
		place_of_birth = row['place_of_birth']
		folk = row['folk']
		religion = row['religion']
		address = row['address']
		ward = row['ward']
		district = row['district']
		province = row['province']
		temporary_address = row['temporary_address']
		home_phone = row['home_phone']
		mobile_phone = row['mobile_phone']
		email = row['email']

		create_user_by_infomation(	self.request.session['user_id'],
									identify,
									first_name,
									last_name,
									gender,
									date_of_birth,
									place_of_birth,
									folk,
									religion,
									address,
									ward,
									district,
									province,
									temporary_address,
									home_phone,
									mobile_phone,
									email	)

		print '-------------'
		return 'ok'

	def get_context_data(self, **kwargs):
		context = super(UserImportView, self).get_context_data(**kwargs)

		context['title'] = u'Nhập danh sách tài khoản'
		context['page_title'] =  u'Nhập danh sách tài khoản'

		context['user_active'] = 'active'
		
		context['page_breadcrumb'] =  mark_safe(u'<li><i class="fa fa-user"></i><a>Quản lý tài khoản</a><i class="fa fa-angle-right"></i></li><li><i class="icon-login"></i><a> Nhập danh sách tài khoản</a></li>')
		return context