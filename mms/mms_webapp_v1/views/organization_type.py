from django.views.generic import CreateView

from mms_webapp_v1.forms.organization_type import OrganizationTypeForm
from mms_backoffice.models import *

class OrganizationTypeCreateView(CreateView):
	template_name = 'temporary/organization/editor.html'
	#form_class = OrganizationTypeForm
	model = OrganizationType	
	fields = ['name']
	
	# def form_valid(self, form):
	# 	form.submit()
	# 	return super(OrganizationTypeCreateView, self).form_valid(form)

	