# -*- coding: utf-8 -*-

from mms_backoffice.models import *


#region QLTV - Quản lý thành viên


# QLTV - Lấy thông tin của một người dùng bằng mã số dòng trên CSDL hoặc mã định danh (ví dụ: MMSV, CMND)
def __get_user_by_id(user_id):
	# try:
	# 	return User.objects.get(id=int(user_id))
	# except:
	# 	pass
	# if type(user_id) is str or type(user_id) is unicode:
		# Trường hợp 2: Nếu mã là mã định danh của người dùng
	try:
		return User.objects.get(identify=user_id)
	except:
		pass	
	return None



# QLTV - Xác định mã người dùng có tồn tại hay không
def is_user_id_valid(user_id):
	if __get_user_by_id(user_id) is not None:
		return True 
	return False



# QLTV - Xác định mã người dùng có phải là mã của quản trị chính hệ thống (super user) hay không
def is_super_administrator_id(user_id):
	user = __get_user_by_id(user_id)
	if user is not None:
		if user.is_superuser:
			return True
	return False



# QLTV - Xác định một người dùng có là người quản lý tổ chức của một người dùng khác hay không
def is_user_manage_by_organization(manager_id, user_id):
	try:
		manager = __get_user_by_id(manager_id)
		user = __get_user_by_id(user_id)

		print manager
		print user

		# Lấy danh sách tổ chức mà người dùng manager quản lý bao gồm các tổ chức con
		organization_user_list = get_all_manage_organizations(manager_id)

		print organization_user_list

		# Với mỗi tổ chức trong danh sách, xác định người dùng user có tham gia hay không
		for obj in organization_user_list:
			if is_user_in_organization(user_id, obj.identify):
				return True
	except Exception, e:
		print e

	return False



# QLTV - Xác định một người dùng có là người quản lý hoạt động của một người dùng khác hay không
def is_user_manage_by_activity(manager_id, user_id):
	# Lấy danh sách hoạt động mà người dùng manager quản lý
	activity_list = get_user_managed_activities(manager_id)

	# Nếu người dùng user nằm trong danh sách
	try:
		activity_user_list = ActivityUser.objects.filter(user=user_id, activity__in=activity_list)
		if len(activity_user_list) > 0:
			return True
	except:
		pass

	return False



# QLTV - Xác định một người dùng có thể truy cập thông tin cá nhân của một người dùng khác bằng mã người dùng hay không 
def can_get_user(user_id, accessed_user_id):
	user = __get_user_by_id(user_id)		
	accessed_user = __get_user_by_id(accessed_user_id)

	if user is None or accessed_user is None:
		return False

	# Trường hợp 1: Người truy cập là quản trị chính hệ thống
	if user.is_superuser:
		return True

	# Trường hợp 2: Người truy cập là người được truy cập
	if user.id == accessed_user.id:
		return True

	# Trường hợp 3: Người truy cập là người quản lý tổ chức của người được truy cập
	if is_user_manage_by_organization(user_id, accessed_user_id):
		return True

	# Trường hợp 4: Người truy cập là người quản lý hoạt động của người được truy cập
	if is_user_manage_by_activity(user_id, accessed_user_id):
		return True

	return False



# QLTV - Xác định một người dùng có thể thay đổi thông tin cá nhân của một người dùng khác bằng mã người dùng hay không 
def can_set_user(user_id, accessed_user_id):
	user = __get_user_by_id(user_id)
	accessed_user = __get_user_by_id(accessed_user_id)

	if user is None or accessed_user is None:
		return False

	# Trường hợp 1: Người truy cập là quản trị chính hệ thống
	if user.is_superuser:
		return True

	# Trường hợp 2: Người truy cập là người được truy cập
	if user.id == accessed_user.id:
		return True

	return False



# QLTV - Lấy thông tin của một người dùng
def get_user(user_id, accessed_user_id):
	if can_get_user(user_id, accessed_user_id):
		return __get_user_by_id(accessed_user_id)
	return None



# QLTV - Đặt lại mật khẩu của một người dùng
def reset_user_password(user_id, accessed_user_id):
	if can_set_user(user_id, accessed_user_id):
		user = __get_user_by_id(accessed_user_id)
		user.set_password(user.identify)
		user.save()
		return True
	return False


# QLTV - Tạo/Chỉnh sửa một người dùng
def set_user(
	user_id,
	user_identify,
	first_name=None,
	last_name=None,
	gender=None,
	date_of_birth=None,
	place_of_birth=None,
	folk=None,
	religion=None,
	address=None,
	ward=None,
	district=None,
	province=None,
	temporary_address=None,
	home_phone=None,
	mobile_phone=None,
	email=None):

	
	identify_type = type(user_identify)	
	print identify_type
	try:
		if identify_type is str or identify_type is unicode: 
			user = __get_user_by_id(user_identify)
			if user is None:
				if is_super_administrator_id(user_id):
					user = User(
						identify=user_identify,
						first_name=first_name,
						last_name=last_name,
						gender=gender,
						date_of_birth=date_of_birth,
						place_of_birth=place_of_birth,
						folk=folk,
						religion=religion,
						address=address,
						ward=ward,
						district=district,
						province=province,
						temporary_address=temporary_address,
						home_phone=home_phone,
						mobile_phone=mobile_phone,
						email=email )
					user.set_password(user.identify)
					user.save()
					return True
			else:
				if can_set_user(user_id, user_identify):
					user.first_name = first_name
					user.last_name = last_name
					user.gender = gender
					user.date_of_birth = date_of_birth
					user.place_of_birth = place_of_birth
					user.folk = folk
					user.religion = religion
					user.address = address
					user.ward = ward
					user.district = district
					user.province = province
					user.temporary_address = temporary_address
					user.home_phone = home_phone
					user.mobile_phone = mobile_phone
					user.email = email 
					user.save()
					return True
		else:
			user = __get_user_by_id(user_identify.identify)
			if user is None:
				if is_super_administrator_id(user_id):
					print user_identify.password
					if user_identify.password is None or len(user_identify.password) == 0:
						user_identify.set_password(user_identify.identify)
					else:
						user_identify.set_password(user_identify.password)
						print user_identify.password
					user_identify.save()
					return True
			else:
				if can_set_user(user_id, user.identify):
					user_identify.save()
					return True
	except Exception, e:
		print e
	return False



# QLTV - Xóa một người dùng
def delete_user(manager_id, user_id):
	if is_super_administrator_id(user_id):
		try:
			user = __get_user_by_id(user_id)
			user.delete()
			return True
		except:
			pass
	return False



# QLTV - Lấy danh sách tất cả người dùng
def get_user_list(user_id):
	if is_super_administrator_id(user_id):
		return User.objects.all()
	return None



def get_user_activity_list(manager_id, user_id):
	if can_get_user(manager_id, user_id):
		user = __get_user_by_id(user_id)

		ids = []
		object_list = ActivityUserPermission.objects.filter(user=user)
		for obj in object_list:
			ids.append(obj.activity.identify)
		object_list = ActivityUser.objects.filter(user=user, state__lte=5)
		for obj in object_list:
			ids.append(obj.activity.identify)

		return Activity.objects.all().filter(identify__in=ids)

	return None

#QLTV - Lấy User model
def get_user_model():

	return User



#endregion



#region QLLTC - Quản lý loại tổ chức



# QLLTC - Lấy một loại tổ chức
def __get_organization_type_by_id(organization_type_id):
	# if type(organization_type_id) is int:
	# 	try:
	# 		return OrganizationType.objects.get(id=organization_type_id)
	# 	except:
	# 		pass
	# else:
	# 	if type(organization_type_id) is str or type(organization_type_id) is unicode:
	# 		# Trường hợp 2: Nếu mã là mã định danh của tổ chức
	try:
		return OrganizationType.objects.get(identify=organization_type_id)
	except:
		pass
	return None 



# QLLTC - Tạo một loại tổ chức
def create_organization_type(user_id, identify, name, management_level):
	if is_super_administrator_id(user_id):
		try:
			organization_type_object = OrganizationType(identify=identify, name=name, management_level=management_level)
			organization_type_object.save()
			return True
		except:
			pass
	return False



# QLLTC - Lấy một loại tổ chức
def get_organization_type(organization_type_id):

	return __get_organization_type_by_id(organization_type_id)



# QLLTC - Xóa một loại tổ chức
def delete_organization_type(user_id, organization_type_id):
	if is_super_administrator_id(user_id):
		organization_type = __get_organization_type_by_id(organization_type_id)
		organization_list = Organization.objects.filter(organization_type=organization_type)
		if len(organization_list) > 0:
			return False
		organization_type.delete()
		return True
	return False



# QLLTC - Sửa loại tổ chức
def set_organization_type(user_id, organization_type_id):
	if is_super_administrator_id(user_id):

		return __get_organization_type_by_id(organization_type_id)
	return None




# QLLTC - Sửa loại tổ chức
def set_organization_type(user_id, organization_type_object):
	if is_super_administrator_id(user_id):
		organization_type_object.save()
		return True
	return False



# QLLTC - Lấy danh sách loại tổ chức
def get_organization_type_list(user_id):

	return OrganizationType.objects.all()



# QLTC - Lấy OrganizationType model
def get_organization_type_model():
	
	return OrganizationType



#endregion



# region QLCV - Quản lý các chức vụ được quy định theo loại tổ chức

#endregion



#region QLTC - Quản lý tổ chức



# QLTC - Lấy một tổ chức
def __get_organization_by_id(organization_id):
	# try:
	# 	return Organization.objects.get(id=int(organization_id))
	# except Exception, e:
	# 	print e
	# if type(organization_id) is str or type(organization_id) is unicode:
	try:
		return Organization.objects.get(identify=organization_id)
	except:
		pass
	return None



# QLTC - Xác định một người dùng có khả năng là một người điều hành tổ chức
def is_organization_manager(user_id, organization_id=None):
	if is_super_administrator_id(user_id):
		return True
	if organization_id is None:
		try:
			user = __get_user_by_id(user_id)
			organization_user = OrganizationUser.objects.filter(user=user, permission__lte=1)
			if len(organization_user) > 0:
				return True	
		except Exception, e:
			print e
	else:
		try:
			user = __get_user_by_id(user_id)
			organization = __get_organization_by_id(organization_id)
			return __scan_is_organization_manager(user, organization)	
		except Exception, e:
			print e

	return False

def __scan_is_organization_manager(user, organization):
	if organization.identify == 'root':
		return False
	try:
		organization_user_object = OrganizationUser.objects.get(user=user, organization=organization, permission__lte=1)
		if organization_user_object is not None:
			return True
	except Exception, e:
		print e
	return __scan_is_organization_manager(user, organization.manager_organization)



# QLTC - Xác định một người dùng có khả năng là một người quản trị tổ chức
def is_organization_administrator(user_id, organization_id=None):
	if is_super_administrator_id(user_id):
		return True
	print user_id
	if organization_id is None:
		try:
			user = __get_user_by_id(user_id)
			organization_user = OrganizationUser.objects.filter(user=user, permission=0)
			if len(organization_user) > 0:
				return True	
		except Exception, e:
			print e
	else:
		try:
			user = __get_user_by_id(user_id)
			organization = __get_organization_by_id(organization_id)
			return __scan_is_organization_administrator(user, organization)	
		except Exception, e:
			print e
	return False

def __scan_is_organization_administrator(user, organization):
	if organization.identify == 'root':
		return False
	try:
		organization_user_object = OrganizationUser.objects.get(user=user, organization=organization, permission=0)
		return True
	except:
		pass
	return __scan_is_organization_administrator(user, organization.manager_organization)



# QLTC - Xác định một người dùng có thuộc một tổ chức hay không
def is_user_in_organization(user_id, organization_id):
	try:
		user = __get_user_by_id(user_id)
		organization = __get_organization_by_id(organization_id)

		organization_user = OrganizationUser.objects.get(user=user, organization=organization)
		if organization_user is not None:
			return True		
	except:
		pass

	return False



# QLTC - Xác định một người dùng có quyền lấy thông tin của một tổ chức hay không
def can_get_organization(user_id, organization_id):
	# Trường hợp 1: Người dùng là quản trị chính
	if is_super_administrator_id(user_id):
		return True

	# Trường hợp 2: Người dùng có tham gia tổ chức
	if is_user_in_organization(user_id, organization_id):
		return True

	# Trường hợp 3: Người dùng là quản lý của tổ chức
	if is_organization_manager(user_id, organization_id):
		return True

	return False



# QLTC - Xác định một người dùng có quyền chỉnh sửa thông tin của một tổ chức
def can_set_organization(user_id, organization_id):
	# Trường hợp 1: Người dùng là quản trị chính
	if is_super_administrator_id(user_id):
		return True

	# Trường hợp 2: Người dùng là quản trị của tổ chức
	if is_organization_administrator(user_id, organization_id):
		return True

	return False



# QLTC - Lấy thông tin của một tổ chức
def get_organization(organization_id):
	return __get_organization_by_id(organization_id)



# QLTC - Sửa thông tin của một tổ chức
def set_organization(user_id, organization_id):
	if can_set_organization(user_id, organization_id):
		return __get_organization_by_id(organization_id)

	return None



# QLTC - Lấy thông tin của tổ chức gốc
def get_organization_root():
	organization_object = None
	organization_object = __get_organization_by_id('root')
	if organization_object is None:
		organization_object = Organization(identify='root')
		organization_object.save()
	return organization_object



# QLTC - Tạo một tổ chức
def create_organization(user_id, identify, name, organization_type_id):
	# Xác định người dùng có quyền quản trị tổ chức
	if is_organization_administrator(user_id):
		root = get_organization_root()
		try:
			organization_object = Organization(identify=identify, name=name, manager_organization=root, organization_type=__get_organization_type_by_id(organization_type_id))
			organization_object.save()
			organization_user_object = OrganizationUser(organization=organization_object, user=User.objects.get(id=user_manager_id), permission=0)
			organization_user_object.save()
		except Exception as e:
			print e
			return False



# QLTC - Tạo một tổ chức bằng đối tượng
def create_organization(user_id, organization_object):
	# Xác định người dùng có quyền quản trị tổ chức
	if is_organization_administrator(user_id):
		root = get_organization_root()
		try:
			if organization_object.manager_organization is None:
				organization_object.manager_organization = root
			else:
				if organization_object.organization_type.management_level > organization_object.manager_organization.organization_type.management_level:
					return False
			organization_object.save()
			organization_user_object = OrganizationUser(organization=organization_object, user=User.objects.get(id=user_manager_id), permission=0)
			organization_user_object.save()
		except Exception as e:
			print e
			return False



# QLTC - Xóa một tổ chức
def delete_organization(user_id, organization_id):
	organization = __get_organization_by_id(organization_id)
	if organization is not None:
		organization_root = __get_organization_by_id(organization_type_id).manager_organization
		if is_organization_administrator(user_id, organization_root.id):
			# Xóa tất cả thành viên trong tổ chức
			organization_user_list = OrganizationUser.objects.filter(organization=organization)
			for obj in organization_user_list:
				obj.delete()
			return True
	return False



# QLTC - Lấy danh sách tổ chức mà một người dùng tham gia trực tiếp
def get_paticipate_organizations(user_id):
	try: 
		user = __get_user_by_id(user_id)
		organization_user_list = OrganizationUser.objects.filter(user=user)
		objects = []
		for obj in organization_user_list:
			objects.append(obj.organization)
		return objects
	except:
		pass
	return None



# QLTC - Lấy tất cả các tổ chức được quản lý
def __scan_get_all_manage_organizations_by_id(organization_id):
	organization = __get_organization_by_id(organization_id)
	organization_list = Organization.objects.filter(manager_organization=organization)
	objects = []
	for obj in organization_list:
		objects += __scan_get_all_manage_organizations_by_id(obj.identify)
	objects.append(organization_id)
	return objects



# QLTC - Lấy danh sách tổ chức mà một người dùng quản lý bao gồm các tổ chức con
def get_all_manage_organizations(user_id):
	try: 
		user = __get_user_by_id(user_id)
		organization_user_list = OrganizationUser.objects.filter(user=user, permission__lte=1)
		identifies = []
		for obj in organization_user_list:
			identifies += __scan_get_all_manage_organizations_by_id(obj.organization.identify)
		return Organization.objects.all().filter(identify__in=identifies)
	except Exception, e:
		print e
	return None



# QLTC - Lấy danh sách tổ chức mà một người dùng quản trị bao gồm các tổ chức con
def get_all_administrate_organizations(user_id):
	try: 
		user = __get_user_by_id(user_id)
		organization_user_list = OrganizationUser.objects.filter(user=user, permission=0)
		identifies = []
		for obj in organization_user_list:
			identifies += __scan_get_all_manage_organizations_by_id(obj.organization.identify)
		return Organization.objects.all().filter(identify__in=identifies)
	except Exception, e:
		print e
	return None



# QLTC - Lấy danh sách tất cả các tổ chức
def get_organization_list(user_id):
	if is_super_administrator_id(user_id):
		return Organization.objects.all()
	return None



# QLTC - Lấy danh sách người dùng mà một người dùng quản lý trực tiếp trong các tổ chức
def get_user_in_all_user_managed_organizations(user_id):
	try:
		organization_list = get_user_managed_organizations(user_id)

		organization_user_list = OrganizationUser.objects.filter(organization__in=organization_list).values('user').distinct()
		objects = []
		for obj in organization_user_list:
			objects.append(obj.user)

		return objects
	except:
		pass

	return None



# QLTC - Lấy tất cả các người dùng mà người dùng quản lý trong các tổ chức bao gồm các tổ chức con
def get_all_user_in_all_user_managed_organizations(user_id):
	try:
		organization_list = get_all_user_managed_organizations(user_id)

		organization_user_list = OrganizationUser.objects.filter(organization__in=organization_list, flat=True).values('user')

		objects = []
		for obj in organization_user_list:
			objects.append(obj.user)

		return objects
	except:
		pass

	return None



# QLTC - Lấy danh sách người dùng mà một người dùng quản lý trong một tổ chức
def get_user_in_user_managed_organization(user_id, organization_id):
	if not is_organization_manager(user_id, organization_id):
		return None

	user = __get_user_by_id(user_id)
	organization = __get_organization_by_id(organization_id)
	organization_user_list = OrganizationUser.objects.filter(user=user, organization=organization)
	objects = []
	for obj in organization_user_list:
		objects.append(obj.user)

	return objects




# QLTC - Lấy danh sách người dùng mà một người dùng quản lý trong một tổ chức bao gồm các tổ chức con
def get_all_user_in_user_managed_organization(user_id, organization_id):
	if not is_organization_manager(user_id, organization_id):
		return None
	organization = __get_organization_by_id(organization_id)
	organization_list = get_all_manage_organizations(organization.identify)
	organization_user_list = OrganizationUser.objects.filter(organization__in=organization_list)

	ids = []
	for obj in organization_user_list:
		ids.append(obj.user.identify)

	user_list = User.objects.filter(identify__in=ids)

	return user_list



# QLTC - Tạo một quản lý tổ chức
def create_organization_managerment(user_id, manager_organization_id, managed_organization_id):
	try:
		manager = __get_organization_by_id(manager_organization_id)
		managed = __get_organization_by_id(managed_organization_id)

		if can_set_organization(user_id, manager.id) and can_set_organization(user_id, managed.id):
			
			if (manager.organization_type.management_level < managed.organization_type.management_level):
				managed.manager_organization = manager
				managed.save()

	except Exception as e:
		return False



# QLTC - Thêm một người dùng vào tổ chức
def add_organization_user(manager_id, organization_id, user_id, permission=2):
	if not is_organization_administrator(manager_id, organization_id):
		return False

	user = __get_user_by_id(user_id)
	if user is not None:
		organization_user_object = OrganizationUser(organization=organization_id, user=user, permission=permission)
		organization_user_object.save()
		return True

	return False



# QLTC - Lấy một bảng danh sách tổ chức dạng cây (bao gồm các tổ chức con)
def get_organization_tuple_table(user_id, organization_id=None):
	organization = None
	if organization_id is None:
		organization = get_organization_root()
	else:	
		organization = __get_organization_by_id(organization_id)
	return __get_organization_tuple_table(organization)
	
def __get_organization_tuple_table(organization):
	organization_list = Organization.objects.filter(manager_organization=organization)

	objects = []
	for obj in organization_list:
		objects.append(__get_organization_tuple_table(obj))

	return (organization, objects)



# QLTC - Thêm một hoạt động vào tổ chức
def set_organization_activity(	
	user_id,
	organization_id,
	activity_identify,
	activity_name,
	activity_type,
	description=None,
	start_time=None,
	end_time=None,
	register_start_time=None,
	register_end_time=None,
	register_state=None,
	published=False	):

	if not is_organization_manager(user_id, organization_id):
		return False

	try:
		organization = __get_organization_by_id(organization_id)
		user = __get_user_by_id(user_id)

		activity_object = __get_activity_by_id(identify)
		activity_type = __get_activity_type_by_id(activity_type)

		if activity_object is None:
			activity_object = Activity(	
				identify=activity_identify, 
				name=activity_name,
				activity_type=activity_type,
				organization=organization,
				description=description,
				start_time=start_time,
				end_time=end_time,
				register_start_time=register_start_time,
				register_end_time=register_end_time,
				register_state=register_state,
				published=published)
			activity_object.save()
			activity_user_permisstion_object = ActivityUserPermission(user=user, activity=activity_object, permission=0)
			activity_user_permisstion_object.save()
			return True
		else:
			if is_activity_administrator(user_id, activity_id):
				activity_object.name = activity_name
				activity_object.activity_type = activity_type
				activity_object.organization = description
				activity_object.description = details
				activity_object.start_time = start_time
				activity_object.end_time = end_time
				activity_object.register_start_time = register_start_time
				activity_object.register_end_time = register_end_time
				activity_object.register_state = register_state
				activity_object.published = published
				activity_object.save()
				return True
	except Exception, e:
		print e
		
	return False



# QLTC - Thêm một hoạt động vào tổ chức
def set_organization_activity(user_id, organization_id, activity_object):
	if not is_organization_manager(user_id, organization_id):
		return False

	try:
		organization = __get_organization_by_id(organization_id)
		activity_object = __get_activity_by_id(activity_object.identify)

		if activity_object is None:
			activity_object.organization = organization
			activity_object.save()

			user = __get_user_by_id(user_id)
			activity_user_permisstion_object = ActivityUserPermission(user=user, activity=activity_object, permission=0)
			activity_user_permisstion_object.save()
			return True
		else:
			if is_activity_administrator(user_id, activity_id):
				activity_object.save()
				return True
	except Exception, e:
		print e
		
	return False



# QLTC - Lấy Organization model
def get_organization_model():
	return Organization



# Lấy danh sách hoạt động trong một tổ chức
def get_organization_activity_list(user_id, organization_id):
	organization_activity_list = None
	organization = __get_organization_by_id(organization_id)
	return Activity.objects.filter(organization=organization)

	return objects

#endregion



#region QLLHD - Quản lý loại hoạt động



# QLLTC - Lấy một loại hoạt động
def __get_activity_type_by_id(activity_type_id):
	# if type(activity_type_id) is int:
	# 	try:
	# 		return ActivityType.objects.get(id=activity_type_id)
	# 	except:
	# 		pass
	# else:
	if type(activity_type_id) is str or type(activity_type_id) is unicode:
		try:
			return ActivityType.objects.get(identify=activity_type_id)
		except:
			pass
	return None 



# QLLTC - Tạo một loại tổ chức
def create_activity_type(user_id, identify, name, management_level):
	if is_super_administrator_id(user_id):
		try:
			organization_type_object = OrganizationType(identify=identify, name=name, management_level=management_level)
			organization_type_object.save()
			return True
		except:
			pass
	return False



# QLLTC - Lấy một loại tổ chức
def get_organization_type(activity_type_id):

	return __get_activity_type_by_id(activity_type_id)



# QLLTC - Xóa một loại tổ chức
def delete_organization_type(user_id, organization_type_id):
	if is_super_administrator_id(user_id):
		organization_type = __get_organization_type_by_id(organization_type_id)
		organization_list = Organization.objects.filter(organization_type=organization_type)
		if len(organization_list) > 0:
			return False
		organization_type.delete()
		return True
	return False



#endregion


#region QLHD - Quản lý hoạt động



# QLHD - Lấy một hoạt đông 
def __get_activity_by_id(activity_id):
	# if type(activity_id) is int:
	# 	# Trường hợp 1: Nếu mã là mã số dòng trên CSDL của người dùng
	# 	try:
	# 		return Activity.objects.get(id=activity_id)
	# 	except:
	# 		pass
	# else:
	# if type(activity_id) is str or type(activity_id) is unicode:
	# Trường hợp 2: Nếu mã là mã định danh của người dùng
	try:
		return Activity.objects.get(identify=activity_id)
	except:
		pass	
	return None



# QLHD - Xác nhận người dùng đang là quản trị của hoạt động 
def is_activity_administrator(user_id, activity_id):
	user = __get_user_by_id(user_id)
	activity = __get_activity_by_id(activity_id)

	if user is None or activity is None:
		return False

	organization = activity.organization

	if is_organization_administrator(user_id, organization.identify):
		return True

	try:
		activity_user_permission_object = ActivityUserPermission.objects.filter(user=user, activity=activity, permission=0)
		if activity_user_object is not None:
			return True
	except Exception, e:
		print e

	return True



# QLHD - Lấy danh sách hoạt động mà một người dùng quản lý
def get_user_managed_activities(user_id):
	activity_user_list = ActivityUser.objects.filter(user=user_id, state__lte=1)

	objects = []
	for obj in activity_user_list:
		objects.append(obj)

	return objects



# QLHD - Lấy danh sách người dùng mà một người dùng quản lý trong các hoạt động
def get_user_in_user_managed_activities(user_id):
	organization_list = get_user_managed_activities(user_id)

	organization_user_list = OrganizationUser.objects.filter(organization__in=organization_list)
	objects = []
	for obj in organization_user_list:
		objects.append(obj)

	return objects



# QLHD - Thêm một hoạt động
def create_activity(user_id, activity_identify, activity_name, activity_type_id, organization_id,
	start_time=None, end_time=None, register_start_time=None, register_end_time=None, register_state=3,
	published=False, credits=0,  score=0):
	if is_organization_manager(user_id):
		try:
			activity_type = __get_activity_type_by_id(activity_type_id)
			organization = __get_organization_by_id(organization_id)
			activity = Activity(identify=activity_identify, name=activity_name, activity_type=activity_type,organization=organization, start_time=start_time, end_time=end_time,
				register_start_time=register_start_time, register_end_time=register_end_time, register_state=register_state,
				published=published, credits=credits, score=score)
			activity.save()
			user = __get_user_by_id(user_id)
			activity_user = ActivityUser(user=user, activity=activity, state=0)
			activity_user.save()
			return True
		except Exception, e:
			print e
	return False

def get_activity(activity_identify):
	return __get_activity_by_id(activity_identify)
	
def get_activity_model():
	return Activity

#endregion