from django.contrib.messages.views import SuccessMessageMixin

class BaseSuccessMessageMixin(SuccessMessageMixin):
	def clear_messages(self):
		from django.contrib import messages
		storage = messages.get_messages(self.request)
		for message in storage:
			do_something_with(message)
		storage.used = False
