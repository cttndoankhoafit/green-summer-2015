# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Create your models here.

CONST_GENDERS = (
	(u'Nam', u'Nam'),
	(u'Nữ', u'Nữ')
)

CONST_PERMISSION = (
	(u'Đọc', u'Đọc'),
	(u'Ghi', u'Ghi'),
	(u'Quản trị', u'Quản trị'),
)

#region User

class UserManager(BaseUserManager):
	def create_user(self, identify, password=None, **extra_fields):
		now = timezone.now()
		user = self.model(identify=identify, is_staff=False, is_active=True, is_superuser=False, last_login=now, **extra_fields)
		if password is None:
			password = identify
		user.set_password(password)
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
	USERNAME_FIELD = 'identify'
	REQUIRED_FIELDS = []

	identify = models.CharField(max_length=40, unique=True, db_index=True)

	first_name = models.CharField(u'Tên', max_length=8, null=True, blank=True, default=None)
	last_name = models.CharField(u'Họ', max_length=128, null=True, blank=True, default=None)
	gender =  models.CharField(u'Giới tính', max_length=3, null=True, choices=CONST_GENDERS, default=0)
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

	objects = UserManager()
	active_users = ActiveUser()

	def get_short_name(self):
		return self.identify

	def save(self, *args, **kwargs):
		if self.password is None:
			self.password = self.identify
		else:
			if len(self.password) == 0:
				self.password = self.identify
		self.set_password(self.password)
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
	details = models.CharField(max_length=2048, null=True, blank=True, default=None)

	def __unicode__(self):
		return self.name

class OrganizationManager(models.Model):
	organization_manager = models.ForeignKey(Organization, related_name='organization_manager')
	organization_managed =  models.ForeignKey(Organization, related_name='organization_managed')
	details = models.CharField(max_length=2048, null=True, blank=True, default=None)

	def __unicode__(self):
		return self.organization_manager.name + ' - ' + self.organization_managed.name

	class Meta:
		unique_together = ('organization_manager', 'organization_managed')


class OrganizationUser(models.Model):
	organization = models.ForeignKey(Organization)
	user = models.ForeignKey(User)
	permission = models.CharField(u'Quyền hạn', max_length=8, null=True, choices=CONST_PERMISSION, default=0)
	details = models.CharField(max_length=2048, null=True, blank=True, default=None)
	
	def __unicode__(self):
		return self.organization.name + ' - ' + self.user.last_name + ' ' +self.user.first_name

	class Meta:
		unique_together = ('organization', 'user')

#endregion

#region Activity

class ActivityType(models.Model):
	name = models.CharField(u'Loại hoạt động', max_length=128)
	details = models.CharField(max_length=2048, null=True, blank=True, default=None)

	def __unicode__(self):
		return self.name

class Activity(models.Model):
	name = models.CharField(u'Tên hoạt động', max_length=128)
	activity_type = models.ForeignKey(ActivityType)
	details = models.CharField(max_length=2048, null=True, blank=True, default=None)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	date_published = models.DateTimeField(null=True, blank=True, default=None)

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
	user = models.ForeignKey(User)
	activity = models.ForeignKey(Activity)
	state =  models.CharField(u'Trạng thái', max_length=8, null=True, default=0)

	def __unicode__(self):
		return self.activity.name + ' - ' + self.user.identify

	class Meta:
		unique_together = ('user', 'activity')

#endregion

#region Document

#endregion
