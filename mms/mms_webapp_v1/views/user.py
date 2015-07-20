# -*- coding: utf-8 -*-

from import_export.formats import base_formats
from import_export.resources import modelresource_factory
from import_export.forms import ConfirmImportForm, ImportForm
from import_export.results import RowResult

from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.html import mark_safe
from django.views.generic import ListView, UpdateView, CreateView, DetailView, View, FormView

from django.contrib.auth.forms import PasswordChangeForm

from django.template.response import TemplateResponse

import os
import tempfile

from mms_controller.resources.user import *
from mms_webapp_v1.views.base import *

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
		return get_user(	self.request.session['user_id'],
							self.kwargs['user_id']
						)

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
		return get_user(	self.request.session['user_id'],
							self.request.session['user_id']
						)
		
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
		return set_user(	self.request.session['user_id'],
							self.kwargs['user_id']
						)

class UserProfileUpdateView(BaseUserUpdateView):
	template_name = 'v1/user/edit_profile.html'

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
		return set_user(	self.request.session['user_id'],
							self.request.session['user_id']
						)

class UserResetPasswordView(BaseSuccessMessageMixin, UpdateView):
	template_name = 'v1/user/reset_password.html'
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
		return reset_user_password(self.request.session['user_id'], self.kwargs['user_id'])

class UserPasswordChangeView(BaseSuccessMessageMixin, FormView):
	template_name = 'v1/user/change_password.html'
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

	template_name = 'v1/user/create.html'

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
class UserImportView(View):
	model = get_user_model()
	from_encoding = "utf-8"
	resource_class = get_user_resource()
	process_import = 'user_process_import_view_v1'

	title = 'Nhập dữ liệu thành viên'
	main_title = 'Nhập dữ liệu thành viên'
	fields = [	u'Mã số', 
				u'Tên',
				u'Họ',
				u'Giới tính',
				u'Ngày sinh',
				u'Quê quán',
				u'Dân tộc',
				u'Tôn giáo',
				u'Địa chỉ thường trú',
				u'Xã/Phường/Thị trấn',
				u'Quận/Huyện/Thành phố thuộc tỉnh',
				u'Tỉnh/Thành phố',
				u'Địa chỉ tạm trú',
				u'Điện thoại',
				u'Điện thoại di động',
				u'Email'	]

	from_encoding = "utf-8"
	
	#: import / export formats
	DEFAULT_FORMATS = (
		base_formats.CSV,
		base_formats.XLS,
	)
	formats = DEFAULT_FORMATS
	#: template for import view
	import_template_name = 'v1/import.html'
	resource_class = None

	def get_import_formats(self):
		return [f for f in self.formats if f().can_import()]

	def get_resource_class(self):
		if not self.resource_class:
			return modelresource_factory(self.model)
		else:
			return self.resource_class

	def get_import_resource_class(self):
		return self.get_resource_class()

	def get(self, *args, **kwargs):
		resource = self.get_import_resource_class()()
		context = {}

		import_formats = self.get_import_formats()
		form = ImportForm(import_formats, self.request.POST or None, self.request.FILES or None)

		if self.request.POST and form.is_valid():
			input_format = import_formats[int(form.cleaned_data['input_format'])]()
			import_file = form.cleaned_data['import_file']
			# first always write the uploaded file to disk as it may be a
			# memory file or else based on settings upload handlers
			with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
				for chunk in import_file.chunks():
					uploaded_file.write(chunk)

			# then read the file, using the proper format-specific mode
			with open(uploaded_file.name, input_format.get_read_mode()) as uploaded_import_file:
				# warning, big files may exceed memory
				data = uploaded_import_file.read()

				if not input_format.is_binary() and self.from_encoding:
					data = force_text(data, self.from_encoding)
				dataset = input_format.create_dataset(data)
				




				# Edit data set ???
				print dataset.headers

				print dataset[0]







				result = resource.import_data(dataset, dry_run=True, raise_errors=False)

			context['result'] = result

			if not result.has_errors():
				context['confirm_form'] = ConfirmImportForm(initial={
					'import_file_name': os.path.basename(uploaded_file.name),
					'input_format': form.cleaned_data['input_format'],
				})

		context['form'] = form
		context['opts'] = self.model._meta
		context['fields'] = [f.column_name for f in resource.get_fields()]
		context['process_import'] = self.process_import
		context['title'] = self.title
		context['main_title'] = self.main_title
		context['fields'] = self.fields

		print context['process_import'] 
		return TemplateResponse(self.request, [self.import_template_name], context)

	def post(self, *args, **kwargs ):
		return self.get(self, *args, **kwargs)

class UserProcessImportView(View):
	model = User
	resource_class = get_user_resource()
	redirect_url = 'user_list_view_v1'

	from_encoding = "utf-8"

	#: import / export formats
	DEFAULT_FORMATS = (
		base_formats.CSV,
		base_formats.XLS,
	)

	formats = DEFAULT_FORMATS

	import_template_name = 'v1/import.html'
	resource_class = None

	def get_import_formats(self):
		return [f for f in self.formats if f().can_import()]

	def get_resource_class(self):
		if not self.resource_class:
			return modelresource_factory(self.model)
		else:
			return self.resource_class

	def get_import_resource_class(self):
		
		return self.get_resource_class()

	def post(self, *args, **kwargs ):
		opts = self.model._meta
		resource = self.get_import_resource_class()()

		confirm_form = ConfirmImportForm(self.request.POST)
		if confirm_form.is_valid():
			import_formats = self.get_import_formats()
			input_format = import_formats[
				int(confirm_form.cleaned_data['input_format'])
			]()
			import_file_name = os.path.join(
				tempfile.gettempdir(),
				confirm_form.cleaned_data['import_file_name']
			)
			import_file = open(import_file_name, input_format.get_read_mode())
			data = import_file.read()
			if not input_format.is_binary() and self.from_encoding:
				data = force_text(data, self.from_encoding)
			dataset = input_format.create_dataset(data)

			result = resource.import_data(dataset, dry_run=False, raise_errors=True)

			# Add imported objects to LogEntry
			ADDITION = 1
			CHANGE = 2
			DELETION = 3
			logentry_map = {
				RowResult.IMPORT_TYPE_NEW: ADDITION,
				RowResult.IMPORT_TYPE_UPDATE: CHANGE,
				RowResult.IMPORT_TYPE_DELETE: DELETION,
			}
			content_type_id=ContentType.objects.get_for_model(self.model).pk
			'''
			for row in result:
				LogEntry.objects.log_action(
					user_id=request.user.pk,
					content_type_id=content_type_id,
					object_id=row.object_id,
					object_repr=row.object_repr,
					action_flag=logentry_map[row.import_type],
					change_message="%s through import_export" % row.import_type,
				)
			'''
			success_message = 'Import finished'
			messages.success(self.request, success_message)
			import_file.close()

			return HttpResponseRedirect(self.redirect_url)

#endregion