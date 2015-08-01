# -*- coding: utf-8 -*-

from django import forms

from mms_base.resources import *

class OrganizationForm(forms.ModelForm):


	def __init__(self, params, *args, **kwargs):
		super(OrganizationForm, self).__init__(*args, **kwargs)

		queryset = get_all_manage_organizations(params['user_id'])

		self.fields['management_organization'] = forms.ModelChoiceField(queryset=queryset)

	def clean(self):
		super(OrganizationForm, self).clean()

		return self.cleaned_data

	class Meta:
		model = get_organization_model()
		fields =['identify', 'name', 'short_name', 'organization_type', 'management_organization']


class OrganizationPermissionForm(forms.ModelForm):


	def __init__(self, params, *args, **kwargs):
		super(OrganizationForm, self).__init__(*args, **kwargs)

		# queryset = get_all_manage_organizations(params['user_id'])

		# self.fields['management_organization'] = forms.ModelChoiceField(queryset=queryset)

	def clean(self):
		super(OrganizationForm, self).clean()

		return self.cleaned_data

	class Meta:
		model = get_organization_user_model()
		fields =['user', 'organization', 'permission', 'position']