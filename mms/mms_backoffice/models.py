# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

from django.contrib import admin

# Create your models here.

#region User

class UserManager(BaseUserManager):
	def create_user(self, identify, password=None, **extra_fields):
		now = timezone.now()
		user = self.model(identify=identify, is_staff=False, is_active=True, is_superuser=False, last_login=now, **extra_fields)
		if password is None:
			password = identify
		user.save(using=self._db)
		return user

	def create_superuser(self, identify, password, **extra_fields):
		u = self.create_user(identify, password, **extra_fields)
		u.is_staff = True
		u.is_active = True
		u.is_superuser = True
		u.save(using=self._db)
		return u

class ActiveUser(models.Manager):
	def get_query_set(self):
		return super(ActiveUser, self).get_query_set().filter(is_active=True)

class User(AbstractBaseUser, PermissionsMixin):
	CONST_GENDERS = (
		(0 , u'Nam'),
		(1, u'Nữ')
	)

	USERNAME_FIELD = 'identify'
	REQUIRED_FIELDS = []

	identify = models.CharField(max_length=40, unique=True, db_index=True)

	first_name = models.CharField(u'Tên', max_length=8, null=True, blank=True, default=None)
	last_name = models.CharField(u'Họ', max_length=128, null=True, blank=True, default=None)
	gender =  models.PositiveSmallIntegerField(u'Giới tính', null=True, choices=CONST_GENDERS, default=0)
	date_of_birth = models.DateField(u'Ngày sinh', null=True, blank=True, default=None)
	place_of_birth = models.CharField(u'Nơi sinh', max_length=128, null=True, blank=True, default=None)
	folk = models.CharField(u'Dân tộc', max_length=32, null=True, blank=True, default=None)
	religion = models.CharField(u'Tôn giáo', max_length=32, null=True, blank=True, default=None)
	address = models.CharField(u'Địa chỉ thường trú', max_length=128, null=True, blank=True, default=None)
	ward = models.CharField(u'Xã/Phường/Thị trấn', max_length=128, null=True, blank=True, default=None)
	district = models.CharField(u'Quận/Huyện/Thành phố thuộc tỉnh', max_length=128, null=True, blank=True, default=None)
	province = models.CharField(u'Tỉnh/Thành phố', max_length=128, null=True, blank=True, default=None)
	temporary_address = models.CharField(u'Địa chỉ tạm trú', max_length=128, null=True, blank=True, default=None)
	home_phone = models.CharField(u'Điện thoại', max_length=32, null = True, blank=True, default=None)	
	mobile_phone = models.CharField(u'Điện thoại di động', max_length=32, null = True, blank=True, default=None)
	email = models.EmailField(u'Email', max_length=128, null = True, blank=True, default=None)

	# If the member is a student, add member's admission date
	details = models.CharField(u'Thông tin khác', max_length=2048, null=True, blank=True, default=None)

	is_staff = models.BooleanField('staff status', default=False,
		help_text='Designates whether the user can log into this admin '
				'site.')
	is_active = models.BooleanField('active', default=True,
		help_text='Designates whether this user should be treated as '
						'active. Unselect this instead of deleting accounts.')

	class Meta:
		ordering = ['identify']

	objects = UserManager()
	active_users = ActiveUser()

	def get_short_name(self):
		return self.identify

	def get_full_name(self):
		if self.last_name is None or self.first_name is None:
			return self.identify
		if len(self.last_name) == 0 or len(self.first_name) == 0:
			return self.identify
		return self.last_name + ' ' + self.first_name
	
	def get_address(self):
		if self.address is not None and self.ward is not None and self.province is not None:
			if len(self.address) > 0 and len(self.ward) > 0 and len(self.province) > 0:
				return self.address + ', ' + self.ward + ', ' + self.province
		return ''

	def save(self, *args, **kwargs):
		if self.password is None:
			self.set_password(self.identify)
		else:
			if len(self.password) == 0:
				self.set_password(self.identify)
			# else:
			# 	try:
			# 		user = User.objects.get(identify=self.identify)	
			# 		print self.password
			# 		print user.password
			# 		if self.password != user.password:
			# 			self.set_password(self.password)
			# 	except User.DoesNotExist:
			# 		self.set_password(self.password)
					
		super(User, self).save(*args, **kwargs)

	def __unicode__(self):
		if self.last_name is None or self.first_name is None:
			return self.identify
		return self.identify + ' - ' + self.last_name + ' ' + self.first_name
		
#endregion

#region Organization

class OrganizationType(models.Model):
	name = models.CharField(u'Loại tổ chức', max_length=128)
	details = models.CharField(max_length=2048, null=True, blank=True, default=None)

	def __unicode__(self):
		return self.name

	
class Organization(models.Model):
	name = models.CharField(u'Tên tổ chức', max_length=128)
	organization_type = models.ForeignKey(OrganizationType)
	organization_manager = models.ForeignKey('self', null=True, blank=True, default=None)
	details = models.CharField(max_length=2048, null=True, blank=True, default=None)

	def __unicode__(self):
		return self.name

class OrganizationUser(models.Model):
	CONST_STATES = (
		(0, u'Quản trị'),
		(1, u'Cán bộ chủ chốt'),
		(2, u'Cán bộ'),
		(3, u'Thành viên'),
	)

	organization = models.ForeignKey(Organization)
	user = models.ForeignKey(User)
	state =  models.PositiveSmallIntegerField(u'Trạng thái', null=True, choices=CONST_STATES, default=3)
	details = models.CharField(max_length=2048, null=True, blank=True, default=None)
	
	def __unicode__(self):
		return self.organization.name + ' - ' + self.user.last_name + ' ' +self.user.first_name

	class Meta:
		unique_together = ('organization', 'user')

#endregion

#region Activity

class Activity(models.Model):
	CONST_TYPES = (
		(0, u'Nhận thức'),
		(1, u'Hành động'),
		(2, u'Khác'),
	)

	name = models.CharField(u'Tên hoạt động', max_length=128)
	activity_type =  models.PositiveSmallIntegerField(u'Loại hoạt động', null=True, choices=CONST_TYPES, default=2)
	start_time = models.DateTimeField(null=True, blank=True, default=None)
	end_time = models.DateTimeField(null=True, blank=True, default=None)
	published_time = models.DateTimeField(null=True, blank=True, default=None)

	details = models.CharField(max_length=2048, null=True, blank=True, default=None)

	def __unicode__(self):
		return self.name

class ActivityOrganization(models.Model):
	activity = models.ForeignKey(Activity)
	organization = models.ForeignKey(Organization)

	def __unicode__(self):
		return self.activity.name + ' - ' + self.organization.name

	class Meta:
		unique_together = ('activity', 'organization')

class ActivityUser(models.Model):
	CONST_STATES = (
		(0, u'Quản trị'),
		(1, u'Ban tổ chức'),
		(2, u'Cộng tác viên'),
		(3, u'Đã tham gia'),
		(4, u'Đã đăng ký'),
		(5, u'Rèn luyện Đoàn viên'),
		(6, u'Rèn luyện Hội viên'),
		(7, u'Không tham gia'),
	)

	user = models.ForeignKey(User)
	activity = models.ForeignKey(Activity)
	state =  models.PositiveSmallIntegerField(u'Trạng thái', null=True, choices=CONST_STATES, default=7)

	def __unicode__(self):
		return self.activity.name + ' - ' + self.user.identify + ' - ' + self.CONST_STATES[self.state][1]

	class Meta:
		unique_together = ('user', 'activity', 'state')

class ActivityUserAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		f = ActivityUser.objects.filter(user=request.user, activity=obj.activity, state=0)
		if request.user.is_superuser or len(f) != 0:
			obj.save()

#endregion

#region Document

#endregion
