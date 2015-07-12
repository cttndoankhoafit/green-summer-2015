from import_export import resources
from import_export import fields
from import_export.widgets import DateWidget

from datetime import date

from mms_backoffice.models import *

class UserResource(resources.ModelResource):
	class Meta:
		model = User
		fields = (	'identify',
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
		import_id_fields = ['identify']

		export_order = (	'identify',
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

class OrganizationTypeResource(resources.ModelResource):
	class Meta:
		model =  OrganizationType
		fields = (	'id',
					'name',	)

		export_order = (	'id',
							'name',	)

class OrganizationResource(resources.ModelResource):
	class Meta:
		model = Organization

		fields = (	'id',
					'name',
					'organization_type'	)

class OrganizationManagerResource(resources.ModelResource):
	class Meta:
		model = OrganizationManager

		fields = (	'id',
					'organization_manager',
					'organization_managed',	)

class OrganizationUserResource(resources.ModelResource):
	class Meta:
		model = OrganizationUser
		
		fields = (	'id',
					'organization',
					'user',
					'permission',	)

# class OrganizationMemberResource(resources.ModelResource):
# 	class Meta:
# 		model = OrganizationMember

# class UserResource(resources.ModelResource):
# 	class Meta:
# 		model = User
