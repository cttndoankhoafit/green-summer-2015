from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import View, FormView

from django.core.urlresolvers import reverse

import tempfile

import abc

import csv

from mms_base.resources import *


class ImportForm(forms.Form):
	import_file = forms.FileField()


class BaseImportView(SuccessMessageMixin, FormView):
	form_class = ImportForm

	def clear_messages(self):
		from django.contrib import messages
		storage = messages.get_messages(self.request)
		for message in storage:
			do_something_with(message)
		storage.used = False

	def get_user_id(self):
		return 'sa'

	def check_input_row_valid(self, row):
		row_string = ''
		print 'Checking ...'
		try:
			for field in self.CONST_FIELDS:
				row_string += row[field] + ' '
			print 'Row \' ' + row_string + '\' is valid'
			return True 
		except Exception as e:
			print e

		return False

	@abc.abstractmethod
	def input_row(self, row):
		return False
		
	def form_valid(self, form):
		import_file = form.cleaned_data['import_file']
		# first always write the uploaded file to disk as it may be a
		# memory file or else based on settings upload handlers
		with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
			for chunk in import_file.chunks():
				uploaded_file.write(chunk)
		# then read the file, using the proper format-specific mode
		with open(uploaded_file.name) as csvfile:
			# warning, big files may exceed memory
			reader = csv.DictReader(csvfile)
			i = 1
			for row in reader:
				result = self.input_row(row)
				if not result:
					print 'Row ' + str(i) + ' is invalid'
				i += 1
		return super(BaseImportView, self).form_valid(form)


# class ProvinceImportView(BaseImportView):
# 	"""docstring for """
# 	def __init__(self, arg):
# 		super(, self).__init__()
# 		self.arg = arg
		
class UserImportView(BaseImportView):
	template_name = 'import.html'

	success_message = 'Import user list successfully'

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
		return reverse('crowler_user_import_view')
		
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


class OrganizationTypeImportView(BaseImportView):
	template_name = 'import.html'

	success_message = 'Import organization type list successfully'
		
	CONST_FIELDS = (	'identify',
						'name',
						'management_type'	)

	def get_success_url(self):
		return reverse('crowler_organization_type_import_view')

	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		identify = row['identify']
		name = row['name']
		management_type = row['management_type']

		if set_organization_type(	self.get_user_id(),
									identify,
									name,
									management_type	):
			print 'Import organization type ' + identify + ' successfully'
			print '----------'
			return True

		return False


class OrganizationImportView(BaseImportView):
	template_name = 'import.html'

	success_message = 'Import organization list successfully'

	CONST_FIELDS = (	'identify',
						'name',
						'organization_type',
						'manager_organization'	)

	def get_success_url(self):
		return reverse('crowler_organization_import_view')
		
	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		identify = row['identify']
		name = row['name']
		organization_type = row['organization_type']
		manager_organization = row['manager_organization']

		if manager_organization is not None and len(manager_organization) == 0:
			manager_organization = None

		if set_organization(self.get_user_id(), identify, name, organization_type, manager_organization):
			print 'Import organization ' + identify + ' successfully'
			print '----------'
			return True

		return False


class ActivityTypeImportView(BaseImportView):
	template_name = 'import.html'

	success_message = 'Import activity type list successfully'

	CONST_FIELDS = ('identify',	'name')

	def get_success_url(self):
		return reverse('crowler_activity_type_import_view')
		
	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		identify = row['identify']
		name = row['name']

		if set_activity_type(self.get_user_id(), identify, name):
			print 'Import activity type ' + identify + ' successfully'
			print '----------'
			return True

		return False

class ActivityImportView(BaseImportView):
	template_name = 'import.html'

	success_message = 'Import activity list successfully'

	CONST_FIELDS = (	'identify',
						'name',
						'type',
						'organization',
						'period'	)

	def get_success_url(self):
		return reverse('crowler_activity_import_view')
		
	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		identify = row['identify']
		name = row['name']
		activity_type = row['type']
		organization = row['organization']
		period = row['period']

		if set_activity(self.get_user_id(), identify, name, activity_type, organization, period):
			print 'Import activity ' + identify + ' successfully'
			print '----------'
			return True

		return False


class ActivityUserImportView(BaseImportView):
	template_name = 'import.html'

	success_message = 'Import activity user list successfully'

	CONST_FIELDS = (	'activity',
						'user'	)

	def get_success_url(self):
		return reverse('crowler_activity_user_import_view')
		
	def input_row(self, row):
		if not self.check_input_row_valid(row):
			return False
		
		activity = row['activity']
		user = row['user']
		
		if set_activity_user(user, activity, 2, 1):
			print 'Import activity user ' + activity + ' - ' + user + ' successfully'
			print '----------'
			return True

		return False
