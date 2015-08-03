# -*- coding: utf-8 -*-

from django.db.models import Q
from django.utils import timezone

from mms_base.models import *


#region Quản lý quá trình (Period)

def __get_period(period_identify):
	try:
		return Period.objects.get(identify=period_identify)
	except Exception, e:
		print e
	return None


def get_period_list():
	return Period.objects.all()


#endregion


#region Quản lý người dùng (User model)


# Lấy đối tượng người dùng bằng định danh (Khai báo cơ bản, không sử dụng)
def __get_user(user_identify):
	try:
		return User.objects.get(identify=user_identify)
	except Exception, e:
		print e
	return None


# Kiểm tra định danh người dùng có tồn tại hay không
def is_user_exist(user_identify):
	if __get_user(user_identify):
		return True
	return False


# Kiểm tra người dùng là quản trị hệ thống
def is_super_administrator(user_identify):
	user = __get_user(user_identify)
	if user is not None and user.is_superuser:
		return True
	return False


# Kiểm tra một người dùng có quản lý một người dùng khác hay không
def can_manage_user(manager_identify, user_identify=None):
	if not is_user_exist(manager_identify) or not is_user_exist(user_identify):
		return False
	if is_super_administrator(manager_identify):
		return True
	try:
		# Lấy danh sách tổ chức mà người dùng manager quản lý bao gồm các tổ chức con
		organization_list = get_all_manage_organizations(manager_identify)

		# Với mỗi tổ chức trong danh sách, xác định người dùng user có tham gia hay không
		for obj in organization_list:
			if is_user_in_organization(user_identify, obj.identify):
				return True
	except Exception, e:
		print e

	return False


# Kiểm tra một người dùng có được quyền lấy thông tin người dùng khác
# Điều kiện đúng:
# - Người dùng truy cập phải là quản trị hệ thống
# - Người dùng truy cập là người dùng bị truy cập
# - Người dùng truy cập là quản lý của người dùng bị truy cập
def can_get_user(user_identify, accessed_user_identify=None):
	if not is_user_exist(user_identify) or not is_user_exist(accessed_user_identify):
		return False

	# Trường hợp người truy cập là người được truy cập
	if user_identify == accessed_user_identify:
		return True

	# Trường hợp người truy cập là quản trị hệ thống
	if is_super_administrator(user_identify):
		return True

	# Trường hợp người truy cập là quản lý tổ chức của người được truy cập
	if can_manage_user(user_identify, accessed_user_identify):
		return True

	return False


# Kiểm tra một người dùng có được quyền chỉnh sửa thông tin người dùng khác
# Điều kiện đúng:
# - Người dùng truy cập phải là quản trị hệ thống
# - Người dùng truy cập là người dùng bị truy cập
def can_set_user(user_identify, accessed_user_identify=None):
	if not is_user_exist(user_identify) or not is_user_exist(accessed_user_identify):
		return False

	# Trường hợp người truy cập là người được truy cập
	if user_identify == accessed_user_identify:
		return True

	# Trường hợp người truy cập là quản trị hệ thống
	if is_super_administrator(user_identify):
		return True

	return False


# Lấy thông tin một người dùng
# Điều kiện thực hiện:
# - Người dùng truy cập phải là quản trị hệ thống
# - Người dùng truy cập là người dùng bị truy cập
# - Người dùng truy cập là quản lý của người dùng bị truy cập
def	get_user(user_identify, accessed_user_identify):
	if can_get_user(user_identify, accessed_user_identify):
		return __get_user(accessed_user_identify)
	return None


# Thêm/sửa thông tin một người dùng
# Điều kiện thực hiện:
# - Người dùng truy cập phải là quản trị hệ thống
# - Người dùng truy cập là người dùng bị truy cập
def set_user(
		user_identify,
		obj,
		first_name=None,
		last_name=None,
		gender=None,
		date_of_birth=None,
		place_of_birth=None,
		other_place_of_birth=None,

		identification_card_number=None,
		identification_card_provision_place=None,

		folk=None,
		religion=None,
		nationality=None,

		address=None,
		ward=None,
		district=None,
		province=None,
	
		temporary_address=None,
	
		home_phone=None,
		mobile_phone=None,
		email=None,

		is_youth_union_member=False,
		youth_union_join_date=None,

		is_communist_party_member=False,
		communist_party_join_date=None,

		contact_person_name=None,
		contact_person_address=None,
		contact_person_phone=None,
		contact_person_email=None,
		contact_person_note=None
	):

	identify_type = type(obj)	
	try:
		if identify_type is str or identify_type is unicode: 
			user = __get_user(obj)
			if user is None and is_super_administrator(user_identify):
				user = User(
						identify = obj,
						first_name = first_name,
						last_name = last_name,
						gender = gender,
						date_of_birth = date_of_birth,
						place_of_birth = place_of_birth,
						other_place_of_birth = other_place_of_birth,

						identification_card_number = identification_card_number,
						identification_card_provision_place = identification_card_provision_place,

						folk = folk,
						religion = religion,
						nationality = nationality,

						address = address,
						ward = ward,
						district = district,
						province = province,
	
						temporary_address = temporary_address,
	
						home_phone = home_phone,
						mobile_phone = mobile_phone,
						email = email,

						is_youth_union_member = is_youth_union_member,
						youth_union_join_date = youth_union_join_date,

						is_communist_party_member = is_communist_party_member,
						communist_party_join_date = communist_party_join_date,

						contact_person_name = contact_person_name,
						contact_person_address = contact_person_address,
						contact_person_phone = contact_person_phone,
						contact_person_email = contact_person_email,
						contact_person_note = contact_person_note
					)
				user.set_password(user.identify)
				user.save()
				return True
			elif can_get_user(user_identify, obj.identify):
				user.first_name = first_name
				user.last_name = last_name
				user.gender = gender
				user.date_of_birth = date_of_birth
				user.place_of_birth = place_of_birth
				user.other_place_of_birth = other_place_of_birth

				user.identification_card_number = identification_card_number
				user.identification_card_provision_place = identification_card_provision_place

				user.folk = folk
				user.religion = religion
				user.nationality = nationality

				user.address = address
				user.ward = ward
				user.district = district
				user.province = province
	
				user.temporary_address = temporary_address
	
				user.home_phone = home_phone
				user.mobile_phone = mobile_phone
				user.email = email

				user.is_youth_union_member = is_youth_union_member
				user.youth_union_join_date = youth_union_join_date

				user.is_communist_party_member = is_communist_party_member
				user.communist_party_join_date = communist_party_join_date

				user.contact_person_name = contact_person_name
				user.contact_person_address = contact_person_address
				user.contact_person_phone = contact_person_phone
				user.contact_person_email = contact_person_email
				user.contact_person_note = contact_person_note
				return True
		else:
			user = __get_user(obj.identify)
			if user is None and is_super_administrator(user_identify):
				if obj.password is None:
					obj.password = user.identify
				elif len(obj.password) == 0:
					obj.password = user.identify
				obj.set_password(obj.password)	
				obj.save()
				return True
			elif can_get_user(user_identify, obj.identify):
				obj.save()
				return True
	except Exception, e:
		print e
	return False


# Xóa người dùng
# Điều kiện thực hiện:
# - Người dùng truy cập phải là quản trị hệ thống
def delete_user(user_identify, accessed_user_identify):
	if not is_super_administrator(user_identify):
		return False

	# Chưa xây dựng

	return False



# Đặt lại mật khẩu người dùng
def reset_user_password(user_identify, accessed_user_identify):
	if can_set_user(user_identify, accessed_user_identify):
		user = __get_user(accessed_user_identify)
		user.set_password(user.identify)
		user.save()
		return True
	return False


# Lấy danh sách người 
# Điều kiện thực hiện:
# - Người dùng truy cập phải là quản trị hệ thống
def get_user_list(user_identify):
	if is_super_administrator(user_identify):
		return User.objects.all()
	return None


def get_user_model():

	return User


#endregion


#region Quản lý loại tổ chức (OrganizationType model)


# Lấy đối tượng loại tổ chức bằng định danh (Khai báo cơ bản, không sử dụng)
def __get_organization_type(organization_type_identify):
	try:
		return OrganizationType.objects.get(identify=organization_type_identify)
	except Exception, e:
		print e
	return None


# Kiểm tra một loại tổ chức có thuộc một loại tổ chức khác không
def is_child_organization_type(management_organization_type_identify, organization_type_identify):
	organization_type_object = get_organization_type(organization_type_identify)	
	if organization_type_object == None:
		return False
	if management_organization_type_identify == organization_type_object.identify:
		return True
	return is_child_organization_type(management_organization_type_identify, organization_type_object.identify)


# Lấy thông tin một loại tổ chức 
def get_organization_type(organization_type_identify):

	return __get_organization_type(organization_type_identify)


# Thêm/sửa thông tin một loại tổ chức
# Điều kiện thực hiện:
# - Người dùng truy cập phải là quản trị hệ thống
def set_organization_type(
		user_identify,
		obj,
		name = None,
		management_organzation_type_identify=None
	):
	if not is_super_administrator(user_identify):
		return False

	identify_type = type(obj)
	try:
		if identify_type is str or identify_type is unicode:
			organization_type_object = __get_organization_type(obj)
			if organization_type_object is None:
				organization_type_object = OrganizationType(
												identify = obj,
												name = name,
												management_organzation_type = get_organization_type(management_organzation_type_identify)
											)
				organization_type_object.save()
				return True
			else:
				organization_type_object.name = name
				organization_type_object.management_organzation_type = get_organization_type(management_organzation_type_identify)
				return True
		else:
			organization_type_object = obj
			if get_organization_type(organization_type_object.identify) is None:
				organization_type_object.save()
				return True
			else:
				organization_type_object.save()
				return True
	except Exception, e:
		print e

	return False


# Xóa một loại tổ chức
# Điều kiện thực hiện:
# - Người dùng truy cập phải là quản trị hệ thống
def delete_organization_type(user_identify, organization_type_identify):
	if not is_super_administrator(user_identify):
		return False

	# Chưa xây dựng

	return False


def get_organization_type_list():
	return OrganizationType.objects.all()


def get_organization_type_model():

	return OrganizationType


#endregion


#region Quản lý tổ chức (Organization model)


# Lấy đối tượng tổ chức bằng định danh (Khai báo cơ bản, không sử dụng)
def __get_organization(organization_identify):
	try:
		return Organization.objects.get(identify=organization_identify)
	except Exception, e:
		print e
	return None


# Hàm duyệt kiểm tra người dùng có là quản lý hoạt quản trị tổ chức (Khai báo cơ bản, không sử dụng)
def __scan_is_organization_manager(user, organization, permission):
	if organization is None:
		return False
	try:
		organization_user_object = OrganizationUser.objects.get(user = user, organization = organization, permission__lte = permission)
		if organization_user_object is not None:
			return True
	except Exception, e:
		print e
	return __scan_is_organization_manager(user, organization.management_organization, permission)


# Kiểm tra có tồn tại mã tổ chức hay không
def is_organization_exist(organization_identify):
	if __get_organization(organization_identify) is not None:
		return True
	return False


# Kiểm tra một người dùng có là quản lý tổ chức hay không
# Điều kiện đúng
# - Nếu không có định danh tổ chức: Người dùng là quản lý của một tổ chức bất kỳ
# - Nếu có định danh tổ chức: Người dùng là quản lý của tổ chức có định danh được cung cấp
def is_organization_manager(user_identify, organization_identify = None):
	if is_super_administrator(user_identify):
		return True
	if organization_identify is None:
		try:
			user = __get_user(user_identify)
			organization_user = OrganizationUser.objects.filter(user=user, permission__lte = 1)
			if len(organization_user) > 0:
				return True	
		except Exception, e:
			print e
	else:
		try:
			user = __get_user(user_identify)
			organization = __get_organization(organization_identify)
			return __scan_is_organization_manager(user, organization, 1)	
		except Exception, e:
			print e

	return False


# Kiểm tra một người dùng có là quản trị tổ chức hay không
# Điều kiện đúng
# - Nếu không có định danh tổ chức: Người dùng là quản trị của một tổ chức bất kỳ
# - Nếu có định danh tổ chức: Người dùng là quản trị của tổ chức có định danh được cung cấp
def is_organization_administrator(user_identify, organization_identify = None):
	if is_super_administrator(user_identify):
		return True
	if organization_identify is None:
		try:
			user = __get_user(user_identify)
			organization_user = OrganizationUser.objects.filter(user=user, permission = 0)
			if len(organization_user) > 0:
				return True	
		except Exception, e:
			print e
	else:
		try:
			user = __get_user(user_identify)
			organization = __get_organization(organization_identify)
			return __scan_is_organization_manager(user, organization, 0)	
		except Exception, e:
			print e
	return False


# Kiểm tra một tổ chức có thuộc một tổ chức khác hay không
def is_child_organization(management_organization_identify, organization_identify):
	organization = __get_organization(management_organization_identify)
	if organization is None:
		return False
	if organization.identify == management_organization_identify:
		return True
	return is_child_organization(management_organization_identify, organization.identify)


# Kiểm tra người dùng có nằm trong tổ chức hay không
def is_user_in_organization(user_identify, organization_identify):
	try:
		if not is_user_exist(user_identify) or not is_organization_exist(organization_identify):
			return False
	 
		if __get_organization_user(user_identify, organization_identify) is not None:
			return True

		organization_user_list = __get_organization_user(user_identify)

		for obj in organization_user_list:
			if is_child_organization(organization_identify, obj.organization.identify):
				return True
	except Exception, e:
		print e
	return False


# Kiểm tra người dùng có quyền chỉnh sửa thông tin của một tổ chức
# Điều kiện đúng:
# - Người dùng là quản trị hệ thống
# - Người dùng là quản trị tổ chức
def can_set_organization(user_identify, organization_identify):
	if is_super_administrator(user_identify):
		return True

	if is_organization_administrator(user_identify, organization_identify):
		return True

	return False


# QLTC - Lấy thông tin của tổ chức gốc
def get_organization_root():
	organization_object = None
	organization_object = __get_organization('root')
	if organization_object is None:
		organization_object = Organization(identify='root')
		organization_object.save()
	return organization_object


# Lấy thông tin của một tổ chức
def get_organization(organization_identify):

	return __get_organization(organization_identify)


# Thêm/Sửa thông tin của một tổ chức
# Điều kiện thực hiện:
# - Người dùng phải là một quản trị tổ chức
def set_organization(
		user_identify,
		obj,
		name = None,
		organization_type_identify = None,
		management_organization_identify = None
	):
	
	if not is_organization_administrator(user_identify):
		return False
	try:
		object_type = type(obj)
		user = __get_user(user_identify)
		if object_type is str or object_type is unicode:
			organization_type_object = __get_organization_type(organization_type_identify)
			management_organization_object = __get_organization(management_organization_identify)

			if management_organization_object is not None and not is_organization_administrator(user_identify, management_organization_identify) and not is_child_organization_type(management_organization_object.organization_type.identify, organization_type_identify):
				return False
			
			if management_organization_object is None:
				management_organization_object = get_organization_root()
			
			organization_object = __get_organization(obj)

			if organization_object is None:
				organization_object = Organization(
											identify = obj,
											name = name,
											organization_type = organization_type_object,
											management_organization = management_organization_object
										)

				organization_object.save()

				return True
			elif is_organization_administrator(user_identify, organization_object.identify):
				
				organization_object.name = name
				organization_object.organization_type = organization_type_object
				organization_object.management_organization = management_organization_object

				organization_object.save()
				return True
		else:
			organization_object = __get_organization(obj.identify)
			
			if organization_object is None:

				management_organization_object = obj.management_organization

				if management_organization_object is not None and not is_organization_administrator(user_identify, management_organization_object.identify) and not is_child_organization_type(management_organization_object.organization_type.identify, obj.organization_type.identify):
					return False

				if management_organization_object is None:
					management_organization_object = get_organization_root()

				obj.management_organization = management_organization_object
				obj.save()

				return True
			elif is_organization_administrator(user_identify, obj.identify):

				management_organization_object = obj.management_organization

				if management_organization_object is not None and not is_organization_administrator(user_identify, management_organization_object.identify) and not is_child_organization_type(management_organization_object.organization_type.identify, obj.organization_type.identify):
					return False

				if management_organization_object is None:
					management_organization_object = get_organization_root()

				obj.management_organization = management_organization_object
				obj.save()
				return True
	except Exception, e:
		print e

	return False


# Lấy các tổ chức quản lý
def __scan_get_root_organization_identify_list(organization_identify):
	organization = __get_organization(organization_identify)

	if organization.identify == 'root':
		return []

	ids = __scan_get_root_organization_identify_list(organization.management_organization.identify)

	objects = []
	objects.append(organization_identify)
	objects += ids

	return objects


# Lấy tất cả các tổ chức mà người dùng tham gia
def get_joined_organization_list(user_identify):
	try: 

		user = __get_user(user_identify)
		organization_user_list = OrganizationUser.objects.filter(user=user)

		ids = []
		for obj in organization_user_list:
			ids += __scan_get_root_organization_identify_list(obj.organization.identify)
			if is_organization_manager(user_identify, obj.organization.identify):
				ids += __scan_get_child_organization_identify_list(obj.organization.identify)

		return Organization.objects.filter(identify__in=ids)
	except Exception, e:
		print e
	return None


# Duyệt lấy tất cả các tổ chức được một tổ chức quản lý (Khai báo cơ bản, không sử dụng)
def __scan_get_child_organization_identify_list(organization_identify):
	organization = __get_organization(organization_identify)
	organization_list = Organization.objects.filter(management_organization=organization)
	objects = []
	for obj in organization_list:
		objects += __scan_get_child_organization_identify_list(obj.identify)
	objects.append(organization_identify)
	return objects


# Lấy danh sách tất cả các tổ chức mà một người dùng quản lý
def get_all_manage_organizations(user_identify):
	try: 
		user = __get_user(user_identify)
		organization_user_list = OrganizationUser.objects.filter(user=user, permission__lte=1)

		ids = []
		for obj in organization_user_list:
			ids += __scan_get_child_organization_identify_list(obj.organization.identify)
		return Organization.objects.all().filter(identify__in=ids)
	except Exception, e:
		print e
	return None


def get_child_organizations(organization_identify):
	ids = __scan_get_child_organization_identify_list(organization_identify)
	return Organization.objects.filter(identify__in=ids)


# Lấy danh sách tất cả các tổ chức
def get_organization_list():

	return Organization.objects.filter(~Q(identify='root'))


# Lấy một bảng danh sách tổ chức dưới dạng cây (bao gồm các tổ chức con)
def get_organization_tuple_table(organization_identify=None):
	organization = None
	if organization_identify is None:
		organization = get_organization_root()
	else:	
		organization = __get_organization(organization_identify)
	return __get_organization_tuple_table(organization)


# Duyệt lấy bảng danh sách tổ chức dạng cây (Khai báo cơ bản, không sử dụng)
def __get_organization_tuple_table(organization):
	organization_list = Organization.objects.filter(management_organization=organization)

	objects = []
	for obj in organization_list:
		objects.append(__get_organization_tuple_table(obj))

	return (organization, objects)


# Lấy danh sách hoạt động mà tổ chức tổ chức
def get_organization_activity_list(organization_identify):
	organization = __get_organization(organization_identify)

	if organization is None:
		return []

	return Activity.objects.filter(organization=organization)


def get_organization_staff(organization_identify):
	organization = __get_organization(organization_identify)
	organization_user_list = OrganizationUser.objects.filter(organization=organization, permission__lte=1)

	return organization_user_list


def get_organization_model():

	return Organization


#endregion


#region Quản lý thành viên trong tổ chức (OrganizationUser model)


# Lấy thông tin thành viên trong tổ chức (Khai báo cơ bản, không sử dụng)
# Kết quả trả về:
# - Không có mã tổ chức:
# 	+ Quyền hạn không hợp lệ: Danh sách tổ chức mà thành viên tham gia (OrganizationUser)
#	+ Quyền hạn hợp lệ: Danh sách tổ chức mà thành viên tham gia với quyền hạn được cấp (OrganizationUser)
# - Có mã tổ chức:
#	+ Quyền hạn không hợp lệ: Một đối tượng kiểu OrganizationModel phù hợp với truy vấn với 2 giá trị thành viên và tổ chức
#	+ Quyền hạn hợp lệ: Một đối tượng kiểu OrganizationModel phù hợp với truy vấn với 3 giá trị: thành viên, tổ chức và quyền hạn
def __get_organization_user(user_identify, organization_identify = None, permission=3):
	user = __get_user(user_identify)
	organization = __get_organization(organization_identify)
	try:
		if user is None:
			if organization is None:
				return None
			if permission > 2:
				return Organization.objects.filter(organization=organization)
			return OrganizationUser.objects.filter(organization=organization, permission=permission)

		if organization is None:
			if permission > 2:
				return OrganizationUser.objects.filter(user=user)	
			return OrganizationUser.objects.filter(user=user, permission=permission)

		if permission > 2:
			return OrganizationUser.objects.get(user=user, organization=organization)	
		
		return OrganizationUser.objects.get(user=user, organization=organization, permission=permission)
	except Exception, e:
		print e
	return None



def get_organization_user(user_identify, organization_identify):
	return __get_organization_user(user_identify, organization_identify)



# Lấy danh sách tất cả các thành viên trong tổ chức (bao gồm các tổ chức con)
# Điều kiện:
# - Người truy cập phải là người quản lý tổ chức
def get_organization_user_list(user_identify, organization_identify):
	try:
		if not is_organization_manager(user_identify, organization_identify):
			return None

		organization_list = __scan_get_child_organization_identify_list(organization_identify)

		organization_user_list = OrganizationUser.objects.filter(organization__in=organization_list)

		ids = []
		for obj in organization_user_list:
			ids.append(obj.user.identify)


		organization_user_list = OrganizationUser.objects.filter(organization=__get_organization(organization_identify))

		for obj in organization_user_list:
			ids.append(obj.user.identify)

		user_list = User.objects.filter(identify__in=ids)

		return user_list

	except Exception, e:
		print e
	return None	



def get_organization_user_list_count(organization_identify):
	# Chỉnh sửa lại nội dung hàm

	return len(get_organization_user_list('sa', organization_identify))



# Thêm/sửa thông tin tham gia tổ chức của các thành viên
# Điều kiện thực hiện:
# - Người truy cập phải là quản trị của tổ chức
# Đầu vào:
# - Mã người dùng truy cập
# - obj:
#	+ obj là một chuỗi: Hàm có 5 giá trị đầu vào
#	+ obj là một đối tượng kiểu OrganizationUser: Hàm có 2 giá trị đầu vào
def set_organization_user(
		user_identify,
		obj, 
		member_identify = None,
		permission = 2,
		position = None
	):
	if not is_organization_administrator(user_identify):
		return False
	objects_type = type(obj)
	try:
		if objects_type is str or objects_type is unicode:
			organization_object = __get_organization(obj)
			if organization_object is None:
				return False

			if not is_organization_administrator(user_identify, obj):
				return False

			user = __get_user(member_identify)
			if user is None:
				return False

			organization_user_object = __get_organization_user(member_identify, obj)

			if organization_user_object is None:
				organization_user_object = OrganizationUser(
												organization = organization_object,
												user = user,
												permission = permission,
												position = position
											)
				organization_user_object.save()
				return True
			else:
				organization_user_object.permission = permission
				organization_user_object.user.position = position
				organization_user_object.save()
				return True
		else:
			if not is_organization_administrator(user_identify, obj.organization.identify):
				return False
			obj.save()
			return True
	except Exception, e:
		print e

	return False


def get_organization_user_model():
	return OrganizationUser
#endregion


#region Quản lý loại hoạt động (ActivityType)


# Lấy đối tượng loại hoạt động bằng định danh (Khai báo cơ bản, không sử dụng)
def __get_activity_type(activity_type_identify):
	try:
		return ActivityType.objects.get(identify=activity_type_identify)
	except Exception, e:
		print e
	return None


# Lấy đối tượng loại hoạt động
def get_activity_type(activity_type_identify):
	return __get_activity_type(activity_type_identify)


# Thêm/sửa đối tượng loại hoạt động
def set_activity_type(
		user_identify, 
		obj,
		name = None
	):
	if not is_super_administrator(user_identify):
		return False

	identify_type = type(obj)
	try:
		if identify_type is str or identify_type is unicode:
			activity_type_object = __get_activity_type(obj)
			if activity_type_object is None:
				activity_type_object = ActivityType(
												identify = obj,
												name = name
											)
				activity_type_object.save()
				return True
			else:
				activity_type_object.name = name
				return True
		else:
			obj.save()
			return True
	except Exception, e:
		print e

	return False


def get_activity_type_list():
	return ActivityType.objects.all()

	
def get_activity_type_model():
	return ActivityType

	
#endregion


# region Quản lý hoạt động


# Lấy đối tượng hoạt động bằng định danh (Khai báo cơ bản, không sử dụng) 
def __get_activity(activity_identify):
	try:
		return Activity.objects.get(identify=activity_identify)
	except Exception, e:
		print e
	return None


def is_activity_exist(activity_identify):
	try:
		return Activity.objects.get(identify=activity_identify)
	except Exception, e:
		print e
	return None


# Kiểm tra một người dùng có là quản trị hoạt động hay không
def is_activity_administrator(user_identify, activity_identify):
	if not is_user_exist(user_identify) or not is_activity_exist(activity_identify):
		return False
	if is_super_administrator(user_identify):
		return True
	obj = __get_activity_user(user_identify, activity_identify)
	if obj is not None and obj.permission == 0:
		return True
	return False


# Kiểm tra một người dùng có là người quản lý hoạt động hay không
def is_activity_manager(user_identify, activity_identify):
	if not is_user_exist(user_identify) or not is_activity_exist(activity_identify):
		return False
	if is_super_administrator(user_identify):
		return True
	
	obj = __get_activity_user(user_identify, activity_identify)
	if obj is not None and obj.permission == 0:
		return True
	return False


# Lấy thông tin một hoạt động
def get_activity(activity_identify):
	return __get_activity(activity_identify)


# Thêm/sửa thông tin một hoạt động
# Điều kiện:
# + Người truy cập phải là một quản lý tổ chức
def set_activity(
		user_identify,
		obj,
		name = None,
		activity_type_identify = None,
		organization_identify = None,
		
		period_identify = None,

		start_time = None,
		end_time = None,
	
		position = None,

		register_start_time = None,
		register_end_time = None,
	
		published = False,

		credits = 0,
		score = 0,

		description = None,
	):
	if not is_organization_manager(user_identify):
		return False


	try:
		object_type = type(obj)
		user = __get_user(user_identify)

		if object_type is str or object_type is unicode:
			activity_type_object = __get_activity_type(activity_type_identify)			
			if activity_type_object is None:
				return False


			organization_object = __get_organization(organization_identify)
			if organization_object is None:
				return False

			period_object = __get_period(period_identify)

			activity_object = __get_activity(obj)
			if activity_object is None:
				activity_object = Activity(
										identify = obj,
										name = name,
										activity_type = activity_type_object,
										organization = organization_object,
										
										period = period_object,

										start_time = start_time,
										end_time = end_time,
									
										register_start_time = register_start_time,
										register_end_time = register_end_time,
									
										published = published,

										credits = credits,
										score = score,

										description = description
									)
				activity_object.save()

				activity_user_object = ActivityUser(user=user, activity=activity_object, permission=0)
				activity_user_object.save()

				return True
			elif is_activity_administrator(user_identify, obj):
				activity_object.name = name
				activity_object.activity_type = activity_type_object
				activity_object.organization = organization_object

				activity_object.period = period_object
				
				activity_object.start_time = start_time
				activity_object.end_time = end_time
									
				activity_object.register_start_time = register_start_time
				activity_object.register_end_time = register_end_time
									
				activity_object.published = published

				activity_object.credits = credits
				activity_object.score = score

				activity_object.description = description
				activity_object.save()

				return True
		else:
			activity_object = __get_activity(obj.identify)
			if activity_object is None:

				if obj.activity_type is None or obj.organization is None:
					return False

				obj.save()

				activity_user_object = ActivityUser(user=user, activity=obj, permission=0)
				activity_user_object.save()

				return True
			elif is_activity_administrator(user_identify, obj.identify):
				if obj.activity_type is None or obj.organization is None:
					return False

				obj.save()

				return True
	except Exception, e:
		print e

	return False


def can_register_activity(user_identify, activity_identify):
	activity_user_object = __get_activity_user(user_identify, activity_identify)
	if activity_user_object is not None:
		return False
	activity = __get_activity(activity_identify)
	register_start_time = activity.register_start_time
	register_end_time = activity.register_end_time
	if register_start_time is None or register_end_time is None:
		return False
	now = timezone.now()
	if now >= register_start_time and now <= register_end_time:
		return True
	return False


def get_activity_list():
	return Activity.objects.all()


def get_activity_staff(activity_identify):
	activity = __get_activity(activity_identify)
	activity_user_list = ActivityUser.objects.filter(activity=activity, permission__lte=1)

	return activity_user_list



# Lấy Activity model	
def get_activity_model():

	return Activity


#endregion


# region Quản lý các thành viên trong hoạt động (ActivityUser)


# Lấy đối tượng (hoặc nhiều đối tượng) người tham gia hoạt động (Khai báo cơ bản, không sử dụng)
def __get_activity_user(user_identify, activity_identify):
	try:
		user = __get_user(user_identify)
		activity = __get_activity(activity_identify)
		return ActivityUser.objects.get(user=user, activity=activity)
	except Exception, e:
		print e
	return None



def get_activity_user(user_identify, activity_identify):
	return __get_activity_user(user_identify,  activity_identify)



def is_participated_activity(user_identify, activity_identify):
	activity_user_object = __get_activity_user(user_identify, activity_identify)

	if activity_user_object is None:
		return False

	if activity_user_object.permission >= 1:
		return True

	if not activity_user_object.participated:
		return False

	return True
	
# Lấy danh sách các hoạt động đã tham gia của một người dùng
def get_participated_activity_list(user_identify, accessed_user_identify):
	if not can_get_user(user_identify, accessed_user_identify):
		return None

	user = __get_user(accessed_user_identify)
	if user is None:
		return None

	ids = []
	activity_user_list = ActivityUser.objects.filter(user=user)

	for obj in activity_user_list:
		ids.append(obj.activity.identify)

	return Activity.objects.filter(identify__in=ids)


# Lấy bảng thống kê các hoạt động đã tham gia của một người dùng trong một khoảng thời gian
def get_participated_activity_statistics(user_identify, accessed_user_identify, period_identify):
	if not can_get_user(user_identify, accessed_user_identify):
		return None

	user = __get_user(accessed_user_identify)
	if user is None:
		return None

	# ids = []
	# activity_user_list = ActivityUser.objects.filter(user=user)

	# for obj in activity_user_list:
	# 	ids.append(obj.activity.identify)

	return None


# Lấy danh sách thành viên tham gia hoạt động
# Điều kiện:
# - Người truy cập phải là người quản lý hoạt động
# - Hoạt động phải tồn tại
def get_activity_user_list(user_identify, activity_identify):
	if not is_activity_manager(user_identify, activity_identify):
		return []

	return ActivityUser.objects.filter(activity=__get_activity(activity_identify))


# Thêm/sửa thành viên tham gia hoạt động
def set_activity_user(
		obj,
		activity_identify = None,
		permission = 2,
		position = None,
		participated = False,
		note = None,
	):
	object_type = type(obj)
	try:
		if object_type is str or object_type is unicode:
			user_object = __get_user(obj)
			if user_object is None:
				return False

			activity_object = __get_activity(activity_identify)
			if activity_object is None:
				return False

			activity_user_object = __get_activity_user(obj, activity_identify)
			if activity_user_object is None:
				activity_user_object = ActivityUser(
											user = user_object,
											activity = activity_object,
											permission = permission,
											position = position,
											participated = participated,
											note = note
										)
				activity_user_object.save()
				return True
			else:
				activity_user_object.permission = permission
				activity_user_object.position = position
				activity_user_object.participated = participated
				activity_user_object.note = note
				activity_user_object.save()
				return True
		else:
			obj.save()
			return True
	except Exception, e:
		print e
	return False


# Lấy ActivityUser model
def get_activity_user_model():
	return ActivityUser


# endregion


# region Rèn luyện Đoàn viên


# endregion