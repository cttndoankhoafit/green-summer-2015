# -*- coding: utf-8 -*-

from mms_webapp_v1.forms.file import ImportForm

from django.views.generic import FormView

import tempfile

import abc

import csv

class BaseImportView(FormView):
	form_class = ImportForm

	def check_input_row_valid(self, row):
		row_string = ''
		print 'Checking ...'
		try:
			for field in self.CONST_FIELDS:
				row_string += row[field] + ' '
			print 'Row \' ' + row_string + '\' is valid'
			return True 
		except Exception as e:
			print e

		return False

	@abc.abstractmethod
	def input_row(self, row):
		return False
		
	def form_valid(self, form):
		import_file = form.cleaned_data['import_file']
		# first always write the uploaded file to disk as it may be a
		# memory file or else based on settings upload handlers
		with tempfile.NamedTemporaryFile(delete=False) as uploaded_file:
			for chunk in import_file.chunks():
				uploaded_file.write(chunk)
		# then read the file, using the proper format-specific mode
		with open(uploaded_file.name) as csvfile:
			# warning, big files may exceed memory
			reader = csv.DictReader(csvfile)
			i = 1
			for row in reader:
				result = self.input_row(row)
				if not result:
					print 'Row ' + str(i) + ' is invalid'
				i += 1
		return super(BaseImportView, self).form_valid(form)