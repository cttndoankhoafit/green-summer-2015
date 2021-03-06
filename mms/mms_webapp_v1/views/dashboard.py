# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import logout


class DashboardView(TemplateView):
    # model = Provider
    template_name = 'v1/dashboard.html'

    def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(DashboardView, self).get_context_data(**kwargs)

		context['title'] = u'Trang chủ'
		context['page_title'] = u'Trang chủ'
		context['dashboard_active'] = 'active'

		return context