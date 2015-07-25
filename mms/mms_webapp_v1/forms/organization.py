# -*- coding: utf-8 -*-

from django import forms

from mms_controller.resources_temp import *

class OrganizationForm(forms.ModelForm):

	def __init__(self, params, *args, **kwargs):
		super(OrganizationForm, self).__init__(*args, **kwargs)

		queryset = get_all_administrate_organizations(params['user_id'])
		
		# self.fields['manager_organization'] = forms.ModelChoiceField(queryset=queryset)

	def clean(self):
		super(OrganizationForm, self).clean()

		return self.cleaned_data

	class Meta:
		model = get_organization_model()
		fields =['identify', 'name', 'organization_type']