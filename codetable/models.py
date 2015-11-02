from django.db import models
from django.utils import timezone
from django import forms

class Code(models.Model):
	#code = models.CharField(widget=forms.Textarea)
	code = models.CharField(max_length=20000)
	#code = forms.Textarea()
	#code = 
	lang = models.CharField(max_length=20,default="C")
	hash = models.CharField(max_length=20)
	url_count = models.IntegerField(default=0)
	published_date = models.DateTimeField(blank=True)
	def increment(self):
		value = getattr(self,'url_count') + 1
		setattr(self,'url_count',value)
		return value
	def get_count(self):
		value = getattr(self,'url_count')
		return value
	def publish(self):
		self.published_date=timezone.now()
		self.save()
