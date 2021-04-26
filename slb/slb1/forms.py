from django import forms
from django.db.models import fields
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelChoiceField
from django.forms.models import inlineformset_factory


class CreateUserForm(UserCreationForm):
    
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
		labels = {
		    'username':'UserName',
		    'first_name':'First Name',
		    'last_name': 'Last Name',
		    'email':'Email Address'
		}

	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['username'].required = True


		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None



class EquipmentForm(forms.ModelForm):

    class Meta:
        model = Equipments
        fields = ['name', 'discription', 'quantity', 'image']
        labels = {
            'name':'Equipment name',
            'discription':'Equipment short discription',
            'quantity':'Quantity',
			'image':'Equipment Image'
        }