from django import forms
from django.db import models
from django.contrib.auth.models import User as DJUser
from django.core.validators import validate_email
from django.contrib.auth import authenticate as DjangoUserAuth

class UserForm(forms.Form):
	fname = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input',
                  'placeholder':'First'}))
	lname = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input',
                  'placeholder':'Last'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input',
                  'placeholder':'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'ui input',
                  'placeholder':'Password'}))
	passwordConfirm = forms.CharField(widget=forms.PasswordInput(attrs={'class':'ui input',
                  'placeholder':'Confirm Password'}))
	email = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input',
                  'placeholder':'Email'}))
	authKey = forms.CharField(widget=forms.PasswordInput(attrs={'class':'ui input','placeholder':'Authentication Key'}))

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)

	def is_valid(self):
		return forms.Form.is_valid(self)

	def clean_username(self):
		username = self.cleaned_data['username']
		if len(DJUser.objects.filter(username=username)) != 0:
			raise forms.ValidationError('This username is already taken.')
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			validate_email(email)
		except:
			raise forms.ValidationError('Please enter a valid email.')
		if len(DJUser.objects.filter(email=email)) != 0:
			raise forms.ValidationError('There is already a user with this email.')
		return email

	def clean_authKey(self):
		authKey = self.cleaned_data['authKey']
		if hash(authKey) != -1246657315132479579:
			raise forms.ValidationError('This authorization key is incorrect.')
		return authKey

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input',
                  'placeholder':'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'ui input',
                  'placeholder':'Password'}))
	
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

	def is_valid(self):
		"""
		TODO: fix this. it doesn't actually validate anything yet
		"""
		return forms.Form.is_valid(self)

