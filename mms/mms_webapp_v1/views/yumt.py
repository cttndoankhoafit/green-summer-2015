# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.utils.html import mark_safe

from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView

from django.http import HttpResponseRedirect, HttpResponse, Http404

from django.core.urlresolvers import reverse_lazy, reverse

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_webapp_v1.views.bases.base_view import *

from mms_base.resources import *


class BaseYUMTView(BaseView):

	def get_context_data(self, **kwargs):
		context = super(BaseYUMTView, self).get_context_data(**kwargs)

		context['yumt_active'] = 'active'
		
		return context


class YUMTRegisterView(BaseYUMTView, TemplateView):
	template_name = 'v1/yumt/register/overview.html'

	pass