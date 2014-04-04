from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    def __init__(self,*args,**kwargs):
    	super(ContactForm,self).__init__(*args,**kwargs)