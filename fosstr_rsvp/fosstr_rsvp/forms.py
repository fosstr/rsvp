from django import forms
from models import ATTENDING_CHOICES, Guest, IS_STUDENT_CHOICE
from django.db.models import Q

from validate_email_address import validate_email

VISIBLE_ATTENDING_CHOICES = [choice for choice in ATTENDING_CHOICES if choice[0] != 'no_rsvp']

class RSVPForm(forms.Form):
    your_email = forms.EmailField(required=True)
    receive_email_updates_for_this_event = forms.BooleanField(required=True, initial=True)
    name = forms.CharField(max_length=128,required=True)
    associated_organization = forms.CharField(max_length=128,required=False)
    will_you_be_attending = forms.ChoiceField(choices=VISIBLE_ATTENDING_CHOICES,required=True, initial='yes')
    are_you_a_student = forms.ChoiceField(choices=IS_STUDENT_CHOICE,required=True, initial='no')

    def clean_your_email(self):
    	data = self.cleaned_data['your_email']
    	is_email_valid = validate_email(self.cleaned_data['your_email'], check_mx=True, verify=True)
    	if not is_email_valid:
    		raise forms.ValidationError("This email address could not be verified!")
    	return data