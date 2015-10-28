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
	published_date = models.DateTimeField(blank=True)
	def publish(self):
		self.published_date=timezone.now()
		self.save()
