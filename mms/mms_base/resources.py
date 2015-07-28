# -*- coding: utf-8 -*-

from mms_base.models import *

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
	if not is_user_exist(user_identify) or not is_user_exist(accessed_user_identify):
		return False
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
		identify,
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

		is_youth_union_member=None,
		youth_union_join_date=None,

		is_communist_party_member=None,
		communist_party_join_date=None,

		contact_person_name=None,
		contact_person_address=None,
		contact_person_phone=None,
		contact_person_email=None,
		contact_person_note=None
	):

	identify_type = type(identify)	
	try:
		if identify_type is str or identify_type is unicode: 
			user = __get_user(identify)
			if user is None and is_super_administrator(user_identify):
				user = User(
						identify=identify,
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
			elif can_get_user(user_identify, identify):
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
			user_object = identify
			user = __get_user(user_object.identify)
			if user is None and is_super_administrator(user_identify):
				if user_identify.password is None or len(user_identify.password) == 0:
					user_identify.set_password(user_identify.identify)
				else:
					user_identify.set_password(user_identify.password)
				user_identify.save()
				return True
			elif can_get_user(user_identify, user_object.identify):
				user_object.save()
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
		identify,
		name = None,
		management_organzation_type_identify=None
	):
	if not is_super_administrator(user_identify):
		return False

	if management_organzation_type_identify is not None and get_organization_type(management_organzation_type_identify) is None:
		return False

	identify_type = type(identify)
	try:
		if identify_type is str or identify_type is unicode:
			organization_type_object = __get_organization_type(identify)
			if organization_type_object is None:
				organization_type_object = OrganizationType(
												identify = identify,
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
			organization_type_object = identify
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


def get_organization_type_model():

	return OrganizationType


#endregion


#region Quản lý chức vụ theo loại tổ chức (OrganizationTypePosition model)
def __get_organization_type_position(organization_type_position_identify):
	try:
		return OrganizationTypePosition.objects.get(identify=organization_type_position_identify)
	except Exception, e:
		print e
	return None
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
	if not is_user_exist(user_identify) or not is_organization_exist(organization_identify):
		return False
 
	if __get_organization_user(user_identify, organization_identify) is not None:
		return True

	organization_user_list = __get_organization_user(user_identify)

	for obj in organization_user_list:
		if is_child_organization(organization_identify, obj.organizaton.identify):
			return True

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
		identify,
		name = None,
		organization_type_identify = None,
		management_organization_identify = None
	):
	
	if not is_organization_administrator(user_identify):
		return False
	try:
		object_type = type(identify)
		user = __get_user(user_identify)
		if object_type is str or object_type is unicode:
			organization_type_object = __get_organization_type(organization_type_identify)
			management_organization_object = __get_organization(management_organization_identify)

			if management_organization_object is not None and not is_organization_administrator(user_identify, management_organization_identify) and not is_child_organization_type(management_organization_object.organization_type.identify, organization_type_identify):
				return False
			
			if management_organization_object is None:
				management_organization_object = get_organization_root()
			
			organization_object = __get_organization(identify)

			if organization_object is None:
				organization_object = Organization(
											identify = identify,
											name = name,
											organization_type = organization_type_object,
											management_organization = management_organization_object
										)

				organization_object.save()

				organization_user_object = OrganizationUser(organization=organization_object, user=user, permission=0)
				organization_user_object.save()

				return True
			elif is_organization_administrator(user_identify, organization_object.identify):
				
				organization_object.name = name
				organization_object.organization_type = organization_type_object
				organization_object.management_organization = management_organization_object

				organization_object.save()
				return True
		else:
			organization_object = __get_organization(identify.identify)
			
			if organization_object is None:

				management_organization_object = identify.management_organization

				if management_organization_object is not None and not is_organization_administrator(user_identify, management_organization_object.identify) and not is_child_organization_type(management_organization_object.organization_type.identify, identify.organization_type.identify):
					return False

				if management_organization_object is None:
					management_organization_object = get_organization_root()

				identify.management_organization = management_organization_object
				identify.save()

				organization_user_object = OrganizationUser(organization=identify, user=user, permission=0)
				organization_user_object.save()

				return True
			elif is_organization_administrator(user_identify, identify.identify):

				management_organization_object = identify.management_organization

				if management_organization_object is not None and not is_organization_administrator(user_identify, management_organization_object.identify) and not is_child_organization_type(management_organization_object.organization_type.identify, identify.organization_type.identify):
					return False

				if management_organization_object is None:
					management_organization_object = get_organization_root()

				identify.management_organization = management_organization_object
				identify.save()
				return True
	except Exception, e:
		print e

	return False


# Lấy tất cả các tổ chức mà người dùng tham gia trực tiếp
def get_paticipate_organizations(user_identify):
	try: 
		user = __get_user(user_identify)
		organization_user_list = __get_organization_user(user_identify)
		objects = []
		for obj in organization_user_list:
			objects.append(obj.organization)
		return objects
	except Exception, e:
		print e
	return None


# Duyệt lấy tất cả các tổ chức được quản lý (Khai báo cơ bản, không sử dụng)
def __scan_get_all_manage_organizations(organization_identify):
	organization = __get_organization(organization_identify)
	organization_list = Organization.objects.filter(management_organization=organization)
	objects = []
	for obj in organization_list:
		objects += __scan_get_all_manage_organizations(obj.identify)
	objects.append(organization_identify)
	return objects


# Lấy danh sách tất cả các tổ chức mà một người dùng quản lý
def get_all_manage_organizations(user_identify):
	try: 
		user = __get_user(user_identify)
		organization_user_list = OrganizationUser.objects.filter(user=user, permission__lte=1)

		identifies = []
		for obj in organization_user_list:
			identifies += __scan_get_all_manage_organizations(obj.organization.identify)
		return Organization.objects.all().filter(identify__in=identifies)
	except Exception, e:
		print e
	return None


# Lấy danh sách tất cả các tổ chức
def get_organization_list():

	return Organization.objects.all()


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


def get_organization_model():

	return Organization


#endregion


#region Quản lý thành viên trong tổ chức


# Lấy thông tin thành viên trong tổ chức (Khai báo cơ bản, không sử dụng)
# Kết quả trả về:
# - Không có mã tổ chức:
# 	+ Quyền hạn không hợp lệ: Danh sách tổ chức mà thành viên tham gia (OrganizationUser)
#	+ Quyền hạn hợp lệ: Danh sách tổ chức mà thành viên tham gia với quyền hạn được cấp (OrganizationUser)
# - Có mã tổ chức:
#	+ Quyền hạn không hợp lệ: Một đối tượng kiểu OrganizationModel phù hợp với truy vấn với 2 giá trị thành viên và tổ chức
#	+ Quyền hạn hợp lệ: Một đối tượng kiểu OrganizationModel phù hợp với truy vấn với 3 giá trị: thành viên, tổ chức và quyền hạn
def __get_organization_user(user_identify, organization_identify = None, permission=3):
	try:
		if user_identify is None:
			if organization_identify is None:
				return None
			return OrganizationUser.objects.filter(organization=__get_organization(organization_identify))

		if organization_identify is None:
			if permission > 2:
				return OrganizationUser.objects.filter(user=__get_user(user_identify))
			else:
				return OrganizationUser.objects.filter(user=__get_user(user_identify), permission=permission)

		if permission > 2:
			return OrganizationUser.objects.get(user=__get_user(user_identify), organization=__get_organization(organization_identify))	
		
		return OrganizationUser.objects.get(user=__get_user(user_identify), organization=__get_organization(organization_identify), permission=permission)
	except Exception, e:
		print e
	return None


# Lấy danh sách tất cả các thành viên trong tổ chức (bao gồm các tổ chức con)
# Điều kiện:
# - Người truy cập phải là người quản lý tổ chức
def get_organization_user_list(user_identify, organization_identify):
	if not is_organization_manager(user_identify, organization_identify):
		return None

	organization_list = get_all_manage_organizations(organization_identify)
	organization_user_list = OrganizationUser.objects.filter(organization__in=organization_list)

	ids = []
	for obj in organization_user_list:
		ids.append(obj.user.identify)

	organization_user_list = __get_organization_user(None, organization_identify)

	for obj in organization_user_list:
		ids.append(obj.user.identify)

	user_list = User.objects.filter(identify__in=ids)

	return user_list


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
		position_identify = None
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

			position_object = __get_organization_type_position(position_identify)

			if position_object is not None and position_object.organization_type.identify != organization_object.organization_type.identify:
				return False

			organization_user_object = __get_organization_user(member_identify, obj)

			if organization_user_object is None:
				organization_user_object = OrganizationUser(
												organization = organization_object,
												user = user,
												permission = permission,
												position = position_object
											)
				organization_user_object.save()
				return True
			else:
				organization_user_object.permission = permission
				organization_user_object.user = position_object
				organization_user_object.save()
				return True
		else:
			if not is_organization_administrator(user_identify, obj.organization.identify):
				return False

			position_object = obj.position
			if position_object is not None and position_object.organization_type.identify != obj.organization.organization_type.identify:
				return False

			# organization_user_object = __get_organization_user(obj.user.identify, obj.organization.identify)

			obj.save()
			return True
	except Exception, e:
		print e

	return False



#endregion


# region Quản lý hoạt động


def get_activity_model():

	return Activity


#endregion