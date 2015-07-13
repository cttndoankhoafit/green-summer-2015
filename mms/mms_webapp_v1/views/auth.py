# -*- coding: utf-8 -*-

import urlparse

from django.conf import settings

from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponseRedirect

from django.utils.decorators import method_decorator

from django.views.generic import RedirectView
from django.views.generic.edit import FormView

class LoginView(FormView):
	form_class = AuthenticationForm
	redirect_field_name = REDIRECT_FIELD_NAME
	template_name = 'v1/login.html'

	def get_context_data(self, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)
		context['title'] = u'Đăng nhập'
		
		#context['main_title'] = u'Đăng nhập hệ thống'
		
		return context

	def get_success_url(self):
		if self.success_url:
			redirect_to = self.success_url
		else:
			redirect_to = self.request.REQUEST.get(self.redirect_field_name, '')

		netloc = urlparse.urlparse(redirect_to)[1]
		if not redirect_to:
			redirect_to = settings.LOGIN_REDIRECT_URL
		
		# Security check -- don't allow redirection to a different host.
		elif netloc and netloc != self.request.get_host():
			redirect_to = settings.LOGIN_REDIRECT_URL
		
		return redirect_to

	def form_valid(self, form):
		login(self.request, form.get_user())

		self.request.session['user_id'] = self.request.user.id
		self.request.session['identify'] = self.request.user.identify
		
		return HttpResponseRedirect(self.get_success_url())

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))

	def get_form(self, form_class):
		form = super(LoginView, self).get_form(form_class)
		form.fields['username'].widget.attrs['class'] = 'form-control'
		form.fields['password'].widget.attrs['class'] = 'form-control'
		return form

class LogoutView(RedirectView):
	permanent = False
	url = settings.LOGOUT_REDIRECT_URL

	@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)