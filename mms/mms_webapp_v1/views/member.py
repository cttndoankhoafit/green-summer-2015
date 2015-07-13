# -*- coding: utf-8 -*-

from django.views.generic import ListView, TemplateView, UpdateView

from mms_backoffice.models import User

class MemberListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	def get_queryset(self):
		return None

class MemberProfileView(TemplateView):
	template_name = 'v1/member/profile.html'
	
	def get_context_data(self, **kwargs):
		context = super(MemberProfileView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['member_name'] = User.objects.get(id = self.request.session['user_id']).get_full_name()
		context['member_full_name'] = User.objects.get(id = self.request.session['user_id']).get_full_name()

		return context

class UserUpdateView(UpdateView):
	model = User
	fields =['first_name', 'last_name']
	template_name = 'v1/member/profile.html'
	
	def get_context_data(self, **kwargs):
		context = super(UserUpdateView, self).get_context_data(**kwargs)

		context['title'] = u'Thông tin cá nhân'
		context['page_title'] = u'Thông tin cá nhân'
		
		context['member_name'] = User.objects.get(id = self.request.session['user_id']).get_full_name()
		context['member_full_name'] = User.objects.get(id = self.request.session['user_id']).get_full_name()

		return context

		def get_form(self, form_class):
			form = super(UserUpdateView, self).get_form(form_class)
			form.fields['first_name'].widget.attrs['class'] = 'form-control'
			form.fields['gender'].widget.attrs['class'] = 'form-control'
			return form

	def get_object(self):
		return User.objects.get(id=self.request.session['user_id'])