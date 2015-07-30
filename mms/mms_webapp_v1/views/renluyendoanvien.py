# -*- coding: utf-8 -*-

from django.utils.html import mark_safe
from django.core.urlresolvers import reverse
from django.views.generic import ListView, UpdateView, TemplateView, DetailView, CreateView, View
from django.http import HttpResponseRedirect, Http404

from mms_backoffice.models import Activity, ActivityUser

from mms_webapp_v1.views.bases.message import *
from mms_webapp_v1.views.bases.file import *

from mms_controller.resources.activity import *
from mms_controller.resources_temp import *

from mms_base.resources import *

#from mms_webapp_v1.forms.activity import ActivityForm


class BaseRenluyendoanvienView(View):
	def get_context_data(self, **kwargs):
		context = super(BaseRenluyendoanvienView, self).get_context_data(**kwargs)

		context['activity_id'] = self.kwargs['activity_id']

		return context
		
#Hiển thị các hoạt động cho đoàn viên đăng ký rèn luyện đoàn viên
class Dang_Ky_RLDV(ListView):
	template_name = 'v1/renluyendoanvien/layout_dangky.html'

	def get_context_data(self, **kwargs):
		context = super(Dang_Ky_RLDV, self).get_context_data(**kwargs)

		context['title'] = u'Đăng ký rèn luyện Đoàn viên'
		context['page_title'] = u'Đăng ký rèn luyện Đoàn viên'

		context['renluyendoanvien_active'] = 'active'
		context['renluyendoanvien_dangky_active'] = 'active'

		return context
	def get_queryset(self):
			#Lấy các dòng dữ liệu từ bảng Đánh giá rèn luyện đoàn viên của người dùng session['user_id']

		objects = []
		return objects


#Hiển thị danh sách tự đánh giá rèn luyện đoàn viên của người dùng
class RenLuyenDoanVien_TuDanhGia_ListView(ListView):
	template_name = 'v1/renluyendoanvien/layout_tudanhgia.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(RenLuyenDoanVien_TuDanhGia_ListView, self).get_context_data(**kwargs)

		context['title'] = u'Đánh giá rèn luyện Đoàn viên'
		context['page_title'] = u'Đánh giá rèn luyện Đoàn viên'

		context['renluyendoanvien_active'] = 'active'
		context['renluyendoanvien_tudanhgia_active'] = 'active'

		return context

	def get_color(self, value):
		if value == 0:
			return 'blue'
		elif value == 1:
			return 'green'
		elif value == 2:
			return 'purple'

	def get_queryset(self):
		#Lấy các dòng dữ liệu từ bảng Đánh giá rèn luyện đoàn viên của người dùng session['user_id']

		objects = []
		return objects

#Hiển thị kết quả đánh giá rèn luyện đoàn viên của người dùng
class RenLuyenDoanVien_KetquaDanhGia_ListView(ListView):
	template_name = 'v1/renluyendoanvien/layout_ketquadanhgia.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(RenLuyenDoanVien_KetquaDanhGia_ListView, self).get_context_data(**kwargs)

		context['title'] = u'Đánh giá rèn luyện Đoàn viên'
		context['page_title'] = u'Kết quả đánh giá rèn luyện Đoàn viên'

		context['renluyendoanvien_active'] = 'active'
		context['renluyendoanvien_ketquadanhgia_active'] = 'active'

		return context

	def get_color(self, value):
		if value == 0:
			return 'blue'
		elif value == 1:
			return 'green'
		elif value == 2:
			return 'purple'

	def get_queryset(self):
		#Lấy kết quả đánh giá từ bảng Đánh giá rèn luyện đoàn viên của người dùng session['user_id']

		objects = []
		return objects


class RenLuyenDoanVien_KetquaDanhGia_ListView(ListView):
	template_name = 'v1/renluyendoanvien/layout_ketquadanhgia.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(RenLuyenDoanVien_KetquaDanhGia_ListView, self).get_context_data(**kwargs)

		context['title'] = u'Đánh giá rèn luyện Đoàn viên'
		context['page_title'] = u'Kết quả đánh giá rèn luyện Đoàn viên'

		context['renluyendoanvien_active'] = 'active'
		context['renluyendoanvien_ketquadanhgia_active'] = 'active'

		return context

	def get_color(self, value):
		if value == 0:
			return 'blue'
		elif value == 1:
			return 'green'
		elif value == 2:
			return 'purple'

	def get_queryset(self):
		#Lấy kết quả đánh giá từ bảng Đánh giá rèn luyện đoàn viên của người dùng session['user_id']

		objects = []
		return objects

#Trang đánh giá một đoàn viên của một người quản lí thành viên đó.
class RenLuyenDoanVien_DanhGiaDoanVien_ListView(ListView):
	template_name = 'v1/renluyendoanvien/layout_danhgiadoanvien.html'
	paginate_by = '20'

	def get_context_data(self, **kwargs):
		context = super(RenLuyenDoanVien_KetquaDanhGia_ListView, self).get_context_data(**kwargs)

		context['title'] = u'Đánh giá rèn luyện Đoàn viên'
		context['page_title'] = u'Đánh giá rèn luyện Đoàn viên'
		context['can_manage_user'] =  True

		#context['renluyendoanvien_active'] = 'active'
		#context['renluyendoanvien_ketquadanhgia_active'] = 'active'

		return context

	def get_color(self, value):
		if value == 0:
			return 'blue'
		elif value == 1:
			return 'green'
		elif value == 2:
			return 'purple'

	def get_queryset(self):
		#Lấy kết quả đánh giá từ bảng Đánh giá rèn luyện đoàn viên của người dùng session['user_id']

		objects = []
		return objects