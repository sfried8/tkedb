from django import forms
from django.db import models
from django.contrib.auth.models import User as DJUser
from brothers.models import Brother
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

class MessageEmailForm(forms.Form):
	message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Message','rows':'100','cols':'100'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'ui input','placeholder':'Email Address'}))

	def __init__(self, *args, **kwargs):
		super(MessageEmailForm, self).__init__(*args, **kwargs)

	def is_valid(self):
		
		return forms.Form.is_valid(self)

class MessageForm(forms.Form):
	message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Message','rows':'100','cols':'100'}))

	def __init__(self, *args, **kwargs):
		super(MessageForm, self).__init__(*args, **kwargs)

	def is_valid(self):
		
		return forms.Form.is_valid(self)

class ForgotForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input','placeholder':'Username'}),required=False)
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'ui input','placeholder':'Email'}),required=False)

	def __init__(self, *args, **kwargs):
		super(ForgotForm, self).__init__(*args, **kwargs)

	def is_valid(self):
		
		return forms.Form.is_valid(self)

	def clean_username(self):
		username = self.cleaned_data['username']
		if username != None and username != "":
			if len(DJUser.objects.filter(username=username))==0:
				raise forms.ValidationError("This user does not exist.")
		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if email != None and email != "":
			if len(DJUser.objects.filter(email=email))==0:
				raise forms.ValidationError("No user with this email exists.")
		return email

class newPassForm(forms.Form):
	code = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input','placeholder':'Activation Code'}))
	newPass = forms.CharField(widget=forms.PasswordInput(attrs={'class':'ui input','placeholder':'New Password'}))

	def __init__(self, *args, **kwargs):
		super(newPassForm, self).__init__(*args, **kwargs)

	def is_valid(self):
		
		return forms.Form.is_valid(self)

class EditForm(forms.Form):
	b = None
	def __init__(self, *args, **kwargs):
		b = kwargs.pop('b')
		super(EditForm, self).__init__(*args, **kwargs)
		self.fields['fname'].initial = b.fname
		self.fields['lname'].initial = b.lname
		self.fields['name'].initial = b.name
		self.fields['pc'].initial = b.pc
		self.fields['nickname'].initial = b.nickname
		self.fields['big'].initial = b.big
		
		

	fname = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input'}))
	lname = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input'}))
	name = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input'}))
	pc = forms.IntegerField(widget=forms.TextInput(attrs={'class':'ui input'}))
	nickname = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input'}))
	big = forms.CharField(widget=forms.TextInput(attrs={'class':'ui input'}))

	def is_valid(self):
		return forms.Form.is_valid(self)

	def clean_big(self):
		big = self.cleaned_data["big"]
		if len(Brother.objects.filter(name=big))==0:
			raise forms.ValidationError("Please use big's full name")
		return big


















