# from django import forms

# from mms_backoffice.models import User

# class UserForm(forms.ModelForm):
# 	#there fields are not required, so we don't care about their style
# 	email = forms.EmailField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('email')})))
# 	username = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('username')})))
# 	photo = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('photo')})))
# 	full_name = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('full_name')})))
# 	point = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('point')})))
# 	password = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('password')})))
# 	fb_access_token = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('fb_access_token')})))
# 	fb_uid = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('fb_uid')})))
# 	is_staff = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('is_staff')})))
# 	promotions = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('promotions')})))
# 	last_login = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('last_login')})))
# 	locations = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('locations')})))
# 	providers = forms.CharField(required=False, widget=forms.HiddenInput(attrs=({'class':'form-control', 'placeholder':('providers')})))

# 	#set style for better view
# 	first_name = forms.CharField(widget=forms.TextInput(attrs=({'class':'form-control input-medium', 'placeholder':''})))
# 	last_name = forms.CharField(widget=forms.TextInput(attrs=({'class':'form-control input-medium', 'placeholder':''})))


# 	mobile = forms.CharField(widget=forms.TextInput(attrs=({'class':'form-control input-medium', 'placeholder':_('mobile')})))

# 	address = forms.CharField(widget=forms.TextInput(attrs=({'class':'form-control input-medium', 'placeholder':_('address')})))
# 	address = forms.CharField(widget=forms.TextInput(attrs=({'class':'form-control input-medium', 'placeholder':_('address')})))

# 	def __init__(self, *args, **kwargs):
# 	super(UserForm, self).__init__(*args, **kwargs)


# 	class Meta:
# 	model = ShopeUser
# 	fields = ['first_name', 'last_name', 'email',  'gender', 'dob', 'mobile', 'address']