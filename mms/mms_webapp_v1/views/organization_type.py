from django.views.generic import CreateView, ListView

#from mms_webapp_v1.forms.organization_type import OrganizationTypeForm
from mms_backoffice.models import *

class OrganizationTypeListView(ListView):
	
	template_name = 'temporary/organization_type/list.html'

	def get_queryset(self):
		return OrganizationType.objects.all()

class OrganizationTypeCreateView(CreateView):
	template_name = 'temporary/organization_type/editor.html'
	#form_class = OrganizationTypeForm
	model = OrganizationType	
	fields = ['name']
	
	# def form_valid(self, form):
	# 	form.submit()
	# 	return super(OrganizationTypeCreateView, self).form_valid(form)

	