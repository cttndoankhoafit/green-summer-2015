# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import logout

from mms_backoffice.models import *

class DashboardView(TemplateView):
    # model = Provider
    template_name = 'v1/dashboard.html'

    def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(DashboardView, self).get_context_data(**kwargs)

		context['title'] = u'Bảng làm việc'
		context['page_title'] = u'Bảng làm việc'
		context['dashboard_active'] = 'active'

		context['member_name'] = User.objects.get(id = self.request.session['user_id']).get_full_name()

		return context