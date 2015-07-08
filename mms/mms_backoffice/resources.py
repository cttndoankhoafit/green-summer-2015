from import_export import resources
from import_export import fields
from import_export.widgets import DateWidget

from datetime import date

from mms_backoffice.models import *

class MemberResource(resources.ModelResource):
	class Meta:
		model = Member
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
		fields = ('name')

		export_order = ('name')

class OrganizationResource(resources.ModelResource):
	class Meta:
		model = Organization

		fields = (	'name',
					'organization_type'	)

class OrganizationManagerResource(resources.ModelResource):
	class Meta:
		model = OrganizationManager

		fields = (	'organization_manager',
					'organization_managed',	)

class OrganizationUserManagerResource(resources.ModelResource):
	class Meta:
		model = OrganizationUserManager

class OrganizationMemberResource(resources.ModelResource):
	class Meta:
		model = OrganizationMember