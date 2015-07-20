# -*- coding: utf-8 -*-

from mms_webapp_v1.forms.file import *

from django.views.generic import FormView, View

import os
import tempfile

import abc

import csv

from django.http import HttpResponse

from django.shortcuts import render, redirect

class BaseImportView(FormView):
	form_class = ImportForm
	errors = []

	@abc.abstractmethod
	def input_row(self, row):
		return

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		if form.is_valid():
			import_file = form.cleaned_data['import_file']
			print import_file
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
					if result != 'ok':
						self.errors.append({'line' : i, 'error' : result })
					i += 1
			return redirect(self.success_url)
		
		return render(request, self.template_name, {'form': form})