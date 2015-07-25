from django.views.generic import View

class BaseView(View):
	def get_user_id(self):
		return self.request.session['user_id']