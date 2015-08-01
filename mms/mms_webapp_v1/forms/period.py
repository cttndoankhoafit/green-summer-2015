# -*- coding: utf-8 -*-

from django import forms

from mms_base.resources import *

class ChoosePeriodForm(forms.Form):
	period = forms.ModelChoiceField(queryset=get_period_list())

	def __init__(self, item, *args, **kwargs):
		super(ChoosePeriodForm, self).__init__(*args, **kwargs)
		self.fields['period'].queryset = get_period_list()