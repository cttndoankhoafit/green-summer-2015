from django import forms

from mms_backoffice.models import *

class UserForm(forms.ModelForm):
	password = forms.CharField(required=False, widget=forms.PasswordInput)

	class Meta:
		fields = ['identify', 'is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups', 'password']

	def clean_password(self):
		# Regardless of what the user provides, return the
		# initial value. This is done here, rather than on
		# the field, because the field does not have access
		# to the initial value
		password = self.cleaned_data.get("password")
		if not password:
			return self.initial["password"]
		
		return password

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(User, self).save(commit=False)
		password = self.cleaned_data["password"]

		if user.id is not None:
			if password != self.initial["password"]:
		user.set_password(password)
		if commit:
			user.save()
		else:
			user.set_password(password)

		return user
