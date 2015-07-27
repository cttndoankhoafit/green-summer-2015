# -*- coding: utf-8 -*-

from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.html import mark_safe
from django.views.generic import ListView, UpdateView, CreateView, DetailView, FormView, View, TemplateView

from mms_controller.resources_temp import *

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_webapp_v1.views.bases.base_view import *

from django.http import HttpResponseRedirect

# Tin nhắn gửi về
success_create_user_message = u'Thêm người dùng thành công'
success_update_user_message = u'Cập nhật thông tin thành công'
success_reset_password_message = u'Đặt lại mật khẩu thành công'



# Hàm điều chỉnh truy cập người dùng vào một người dùng khác
def access_user(user_id, accessed_user_id):
	user = get_user(user_id, accessed_user_id)
	if user is None:
		raise PermissionDenied
	return user



# Khung nhìn chung cho việc xem thông tin của một tài khoản
class BaseUserView(BaseView):

	def get_user_account_id(self):
		return self.kwargs['user_id']

	def get_context_data(self, **kwargs):
		context = super(BaseUserView, self).get_context_data(**kwargs)
		context['page_title'] = get_user_model().objects.get(identify=self.get_user_account_id()).get_full_name()

		context['identify'] = self.get_user_account_id()

		return context



# Khung nhìn xem thông tin của một người dùng bất kỳ
# URL: user/user=<user_id>/
class UserDetailView(BaseUserView, DetailView):
	template_name = 'v1/user/profile/overview.html'

	def get_context_data(self, **kwargs):
		if not can_get_user(self.get_user_id(), self.get_user_account_id()):
			raise PermissionDenied

		context = super(UserDetailView, self).get_context_data(**kwargs)

		return context

	def get_object(self):
		return get_user(self.get_user_id(), self.get_user_account_id())



# Khung nhìn xem các hoạt động của một người dùng bất kỳ
# URL: user/user=<user_id>/activity/
class UserActivityView(BaseUserView, ListView):
	template_name = 'v1/user/profile/activity.html'

	def get_context_data(self, **kwargs):
		if not can_get_user(self.get_user_id(), self.get_user_account_id()):
			raise PermissionDenied
			
		context = super(UserActivityView, self).get_context_data(**kwargs)

		return context

	def get_queryset(self):
		return get_user_activity_list(self.get_user_id(), self.get_user_account_id())



class UserActivityStatisticsView(BaseUserView, TemplateView):
	template_name = 'v1/user/profile/activity/statistics.html'

	def get_context_data(self, **kwargs):
		if not can_get_user(self.get_user_id(), self.get_user_account_id()):
			raise PermissionDenied
			
		context = super(UserActivityStatisticsView, self).get_context_data(**kwargs)

		return context



# Khung nhìn chuẩn cho các khung nhìn có dạng mẫu (Form)
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



# Khung nhìn cập nhật thông tin người dùng
# URL: user/user=<user_id>/edit/
class UserUpdateView(BaseUserView, UpdateView, UserFormView):
	template_name = 'v1/user/editor/update.html'

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

	def get_success_url(self):
		return reverse('user_update_view_v1', kwargs={'user_id' : self.get_user_account_id() })

	def get_context_data(self, **kwargs):
		if not can_set_user(self.get_user_id(), self.get_user_account_id()):
			raise PermissionDenied

		context = super(UserUpdateView, self).get_context_data(**kwargs)

		return context

	def form_valid(self,form):
		self.object = form.save(commit=False)
		
		if set_user(self.get_user_id(), self.object):
			if self.get_user_id() == self.object.identify:
				self.request.session['user_full_name'] = self.object.get_full_name()
			self.clear_messages()
			return super(UserUpdateView, self).form_valid(form)			

	def get_object(self):
		return get_user(self.get_user_id(), self.get_user_account_id())



# Khung nhìn đặt lại mật khẩu
class UserPasswordChangeView(BaseUserView, BaseSuccessMessageMixin, FormView):
	template_name = 'v1/user/editor/change_password.html'
	form_class = PasswordChangeForm

	success_message = success_reset_password_message

	account_owner = 0

	def get_success_url(self):
		return reverse('user_password_change_view_v1', kwargs={'user_id' : self.get_user_account_id() })

	def get_context_data(self, **kwargs):
		if not can_set_user(self.get_user_id(), self.get_user_account_id()):
			raise PermissionDenied
			
		context = super(UserPasswordChangeView, self).get_context_data(**kwargs)

		if self.get_user_id() == self.get_user_account_id():
			self.account_owner = 1
			context['account_owner'] = 1

		return context

	def get_object(self):
		return self.request.user

	def get_form_kwargs(self):
		kwargs = super(UserPasswordChangeView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		if self.account_owner:
			form.save()
			self.clear_messages()
			return super(UserPasswordChangeView, self).form_valid(form)

	def form_invalid(self, form):
		if not self.account_owner:
			reset_user_password(self.get_user_id(), self.get_user_account_id())
			self.clear_messages()
			return HttpResponseRedirect(self.get_success_url())



# Khung nhìn tạo một người dùng dành cho người quản trị hệ thống
# URL: user/create/
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

	template_name = 'v1/user/creator.html'

	success_message = success_create_user_message

	def get_success_url(self):
		return reverse('user_list_view_v1')

	def get_context_data(self, **kwargs):
		if not is_super_administrator_id(self.request.session['user_id']):
			raise PermissionDenied
			
		context = super(UserCreateView, self).get_context_data(**kwargs)

		context['page_title'] = u'Tạo tài khoản mới'

		return context

 	def get_form(self, form_class):
		form = super(UserCreateView, self).get_form(form_class)
		form.fields['identify'].widget.attrs['class'] = 'form-control'
		form.fields['password'].widget.attrs['class'] = 'form-control'
		return form

	def form_valid(self, form):
		self.object = form.save(commit=False)
		set_user(self.request.session['user_id'], self.object)
		self.clear_messages()
		return super(UserCreateView, self).form_valid(form)



# Khung nhìn lấy danh sách người dùng dành cho người quản trị hệ thống
# URL: user/list/
class UserListView(ListView, FormView):
	template_name = 'v1/static_pages/list.html'
	paginate_by = '20'

	can_set = False
	
	def get_context_data(self, **kwargs):
		if not is_super_administrator_id(self.request.session['user_id']):
			raise PermissionDenied

		context = super(UserListView, self).get_context_data(**kwargs)

		context['title'] = u'Danh sách tài khoản'
		context['page_title'] = u'Danh sách tài khoản'

		context['user_active'] = 'active'
		context['user_list_active'] = 'active'

		context['theads'] = [	{'name': u'#', 'size' : '10%'},
								{'name': u'Họ và Tên', 'size' : 'auto'},	]

		context['add_link'] = '/user/create/'
		context['import_link'] = '/user/import/'

		context['show_add_button'] = 1
		context['show_delete_button'] = 1
		context['show_import_button'] = 1
		context['show_checkbox'] = 1

		return context

	def get_queryset(self):				
		user_list = get_user_list(self.request.session['user_id'])

		objects = []
		if user_list is not None:
			for obj in user_list:
				values = []	
				values.append(mark_safe('<input type="checkbox" class="checkboxes" value="%s" name="list"/>' % obj.identify))
				values.append(obj.identify)
				values.append(mark_safe(u'<a href="/user/user=%s">%s</a>' % (obj.identify, obj.get_full_name())))
				objects.append(values)
		return objects

	def post(self, request, *args, **kwargs):
		print request.POST
		if 'list' in request.POST:
			todel = request.POST.getlist('list')
			print todel
		return self.get(self, *args, **kwargs) #HttpResponseRedirect(reverse('user_list_view_v1'))



# Khung nhìn nhập danh sách người dùng bằng tập tin dành cho người quản trị hệ thống
# URL: user/import/
class UserImportView(BaseView, BaseImportView):
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

	def get_context_data(self, **kwargs):
		if not is_super_administrator_id(self.get_user_id()):
			raise PermissionDenied

		context = super(UserImportView, self).get_context_data(**kwargs)
		
		context['title'] = u'Nhập danh sách tài khoản'
		context['page_title'] =  u'Nhập danh sách tài khoản'

		context['user_active'] = 'active'

		return context
		
	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
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

		if set_user(	
			self.get_user_id(),
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
			email	):
			print 'Import user ' + identify + ' successfully'
			print '----------'
			return True

		return False