from django.views.generic import ListView

# from mms_backoffice.models import Member

class MemberListView(ListView):
	template_name = 'temporary/member/list.html'
	paginate_by = '10'

	def get_queryset(self):
		return None