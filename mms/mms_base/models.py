# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

from django.contrib import admin

# Create your models here.

# Các cấp truy cập thông tin
CONST_PERMISSIONS = (
		(0, u'Chỉnh sửa thông tin'),
		(1, u'Xem thông tin'),
		(2, u'Không có quyền truy cập'),
	)

CONST_TRAINING_TYPES = (
		(0, u'Nhận thức'),
		(1, u'Hành động'),
		(2, u'Khác'),
	) 

# Dữ liệu quốc gia
class Nation(models.Model):
	identify = models.CharField(max_length=50, unique=True, db_index=True)
	name =  models.CharField(max_length=50)


# Dữ liệu dân tộc
class Folk(models.Model):
	identify = models.CharField(max_length=50, unique=True, db_index=True)
	name =  models.CharField(max_length=50)


# Dữ liệu tôn giáo
class Religion(models.Model):
	identify = models.CharField(max_length=50, unique=True, db_index=True)
	name =  models.CharField(max_length=50)


# Dữ liệu tỉnh/thành
class Province(models.Model):
	identify = models.CharField(max_length=50, unique=True, db_index=True)
	name =  models.CharField(max_length=50)


# Dữ liệu quận/huyện
class District(models.Model):
	identify = models.CharField(max_length=50, unique=True, db_index=True)
	name = models.CharField(max_length=50)
	province = models.ForeignKey(Province)


# Dữ liệu xã/phường/thị trấn
class Ward(models.Model):
	identify = models.CharField(max_length=50, unique=True, db_index=True)
	name = models.CharField(max_length=50)
	district = models.ForeignKey(District)


# Dữ liệu các khóa học
# Sử dụng trong quản lý tổ chức trường học
# class Course(models.Model):
# 	identify = models.CharField(max_length=50, unique=True, db_index=True)
# 	name =  models.CharField(max_length=50)


# Dữ liệu giai đoạn thời gian
class Period(models.Model):
	identify = models.CharField(max_length=16, primary_key=True, db_index=True)
	name = models.CharField(max_length=50, null=True, blank=True, default=None)
	start_time = models.DateField()
	end_time = models.DateField()
	
	def __unicode__(self):
		return self.name


#region Dữ liệu Người dùng

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

	# Thông tin cơ bản
	identify = models.CharField(max_length=50, unique=True, db_index=True)
	first_name = models.CharField(u'Tên', max_length=8, null=True, blank=True, default=None)
	last_name = models.CharField(u'Họ', max_length=128, null=True, blank=True, default=None)
	gender =  models.PositiveSmallIntegerField(u'Giới tính', null=True, choices=CONST_GENDERS, default=0)
	date_of_birth = models.DateField(u'Ngày sinh', null=True, blank=True, default=None)
	
	place_of_birth = models.CharField(max_length=50, null=True, blank=True, default=None)
	other_place_of_birth = models.CharField(max_length=50, null=True, blank=True, default=None)
	
	# place_of_birth = models.ForeignKey(Province, null=True, blank=True, default=None, related_name='place_of_birth_related')
	# other_place_of_birth =  models.ForeignKey(Province, null=True, blank=True, default=None, related_name='other_place_of_birth_related')
	
	
	# Nếu người dùng là một sinh viên, bổ sung thông tin
	# admission_date = models.DateField(u'Ngày nhập học', null=True, blank=True, default=None)
	# course = models.ForeignKey(Course, null=True, default=None)


	# Thông tin chi tiết
	# Chứng minh nhân dân
	identification_card_number = models.CharField(u'Số CMND', max_length=10, null=True, blank=True, default=None)
	identification_card_provision_date =  models.DateField(null=True, blank=True, default=None)
	identification_card_provision_place = models.CharField(max_length=50,  null=True, blank=True, default=None)

	# identification_card_provision_place =  models.ForeignKey(Province, null=True, default=None, related_name='identification_card_provision_place')


	folk = models.CharField(max_length=50, null=True, blank=True, default=None)
	religion = models.CharField(max_length=50, null=True, blank=True, default=None)
	nationality = models.CharField(max_length=50, null=True, blank=True, default=None)

	# folk = models.ForeignKey(Folk, null=True, default=None)
	# religion = models.ForeignKey(Religion, null=True, default=None)
	# nationality = models.ForeignKey(Nation, null=True, default=None)

	# Địa chỉ thường trú
	address = models.CharField(u'Địa chỉ thường trú', max_length=128, null=True, blank=True, default=None)
	ward = models.CharField(u'Xã/Phường/Thị trấn', max_length=128, null=True, blank=True, default=None)
	district = models.CharField(u'Quận/Huyện/Thành phố thuộc tỉnh', max_length=128, null=True, blank=True, default=None)
	province = models.CharField(u'Tỉnh/Thành phố', max_length=128, null=True, blank=True, default=None)
	
	# Địa chỉ tạm trú
	temporary_address = models.CharField(u'Địa chỉ tạm trú', max_length=128, null=True, blank=True, default=None)
	
	home_phone = models.CharField(u'Điện thoại', max_length=32, null = True, blank=True, default=None)
	mobile_phone = models.CharField(u'Điện thoại di động', max_length=32, null = True, blank=True, default=None)
	email = models.EmailField(u'Email', max_length=128, null = True, blank=True, default=None)


	# Nếu người dùng là Đoàn viên
	is_youth_union_member = models.BooleanField(u'Là Đoàn viên', default=False)
	youth_union_join_date =  models.DateField(u'Ngày kết nạp Đoàn', null=True, blank=True, default=None)


	# Nếu người dùng là Đảng viên
	is_communist_party_member = models.BooleanField(u'Là Đảng viên', default=False)
	communist_party_join_date =  models.DateField(u'Ngày kết nạp Đảng', null=True, blank=True, default=None)


	# Thông tin liên lạc với gia đình
	contact_person_name = models.CharField(max_length=128, null=True, blank=True, default=None)
	contact_person_address = models.CharField(max_length=128, null=True, blank=True, default=None)
	contact_person_phone = models.CharField(max_length=32, null=True, blank=True, default=None)
	contact_person_email = models.EmailField(max_length=128, null = True, blank=True, default=None)
	contact_person_note = models.CharField(max_length=256, null=True, blank=True, default=None)


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
		if self.address is not None and self.ward is not None and self.district is not None and self.province is not None:
			return self.address + ', ' + self.ward + ', ' + self.district + ', ' + self.province
		return ''

	def save(self, *args, **kwargs):
		if self.password is None:
			self.set_password(self.identify)
		else:
			if len(self.password) == 0:
				self.set_password(self.identify)

		super(User, self).save(*args, **kwargs)

	def __unicode__(self):
		if self.last_name is None or self.first_name is None:
			return self.identify
		return self.identify + ' - ' + self.last_name + ' ' + self.first_name
		
#endregion


#region Dữ liệu tổ chức


# Loại tổ chức
class OrganizationType(models.Model):
	identify = models.CharField(max_length=50, primary_key=True, db_index=True)
	name = models.CharField(u'Loại tổ chức', max_length=128)
	management_organzation_type = models.ForeignKey('self', null=True, blank=True, default=None)

	def __unicode__(self):
		return self.name


# Dữ liệu tổ chức
class Organization(models.Model):
	identify = models.CharField(max_length=50, primary_key=True, db_index=True)
	name = models.CharField(u'Tên tổ chức', max_length=128)
	short_name =  models.CharField(max_length=30, null=True, blank=True, default=None)
	organization_type = models.ForeignKey(OrganizationType, null=True, default=None)
	management_organization = models.ForeignKey('self', null=True, blank=True, default=None)
	description = models.TextField(null=True, blank=True, default=None)

	def __unicode__(self):
		return self.name


# Dữ liệu người dùng trong tổ chức
class OrganizationUser(models.Model):
	organization = models.ForeignKey(Organization)
	user = models.ForeignKey(User)
	permission =  models.PositiveSmallIntegerField(null=True, choices=CONST_PERMISSIONS, default=2)
	position = models.CharField(max_length=64, null=True, blank=True, default=None)

	def __unicode__(self):
		return self.organization.name + ' - ' + self.user.get_full_name()

	class Meta:
		unique_together = ('organization', 'user')


#endregion


#region Dữ liệu hoạt động


# Dữ liệu loại hoạt động
class ActivityType(models.Model):
	identify = models.CharField(max_length=50, primary_key=True, db_index=True)
	name = models.CharField(u'Tên loại hoạt động', max_length=128, null=True, blank=True, default=None)

	def __unicode__(self):
		return self.name


# Dữ liệu hoạt động
class Activity(models.Model):
	identify = models.CharField(max_length=50, primary_key=True, db_index=True)
	name = models.CharField(max_length=128)
	
	activity_type = models.ForeignKey(ActivityType)
	
	organization = models.ForeignKey(Organization)

	period = models.ForeignKey(Period, null=True, default=None)
	
	start_time = models.DateTimeField(null=True, blank=True, default=None)
	end_time = models.DateTimeField(null=True, blank=True, default=None)
	
	location = models.CharField(max_length=128, null=True, blank=True, default=None)

	register_start_time = models.DateTimeField(null=True, blank=True, default=None)
	register_end_time = models.DateTimeField(null=True, blank=True, default=None)
	
	published = models.BooleanField(default=False)

	credits = models.DecimalField(max_digits=8, decimal_places=4, default=0)
	score = models.DecimalField(max_digits=8, decimal_places=4, default=0)

	description = models.TextField(null=True, blank=True, default=None)

	# Thêm mục điểm rèn luyện
	training_type =  models.PositiveSmallIntegerField(null=True, choices=CONST_TRAINING_TYPES, default=2)

	def __unicode__(self):
		return self.name


# Dữ liệu người dùng tham gia
class ActivityUser(models.Model):
	user = models.ForeignKey(User)
	activity = models.ForeignKey(Activity)
	permission = models.PositiveSmallIntegerField(null=True, choices=CONST_PERMISSIONS, default=2)
	position = models.CharField(max_length=64, null=True, blank=True, default=None)
	note = models.TextField(null=True, blank=True, default=None)
	state = models.CharField(max_length=32, null=True, blank=True, default=None)
	
	self_evaluation_score = models.DecimalField(max_digits=8, decimal_places=4, default=0)
	staff_evaluation_score = models.DecimalField(max_digits=8, decimal_places=4, default=0)

	class Meta:
		unique_together = ('user', 'activity', 'state')
	
	def __unicode__(self):
		return self.activity.name + ' - ' + self.user.identify


#endregion


#region Dữ liệu rèn luyện Đoàn viên
# Dữ liệu thông tin cơ bản của chương trình
class YouthUnionMenberTrainingProgram(models.Model):
	name = models.CharField(max_length=128)
	period = models.ForeignKey(Period, unique=True)

	register_start_time = models.DateTimeField(null=True, blank=True, default=None)
	register_end_time = models.DateTimeField(null=True, blank=True, default=None)

	evaluation_start_time = models.DateTimeField(null=True, blank=True, default=None)
	evaluation_end_time = models.DateTimeField(null=True, blank=True, default=None)

	def __unicode__(self):
		return self.period.name


# Dữ liệu người dùng tham gia chương trình
class YouthUnionMenberTrainingProgramUser(models.Model):
	user = models.ForeignKey(User)
	program = models.ForeignKey(YouthUnionMenberTrainingProgram)

	class Meta:
		unique_together = ('user', 'program')

	def __unicode__(self):
		return self.user.get_full_name() + ' - ' + self.program.name

#endregion