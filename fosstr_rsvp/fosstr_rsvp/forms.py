from django import forms
from models import ATTENDING_CHOICES, Guest, IS_STUDENT_CHOICE, EMAIL_UPDATE_CHOICES
from django.db.models import Q

from validate_email_address import validate_email

VISIBLE_ATTENDING_CHOICES = [choice for choice in ATTENDING_CHOICES if choice[0] != 'no_rsvp']


class RSVPForm(forms.Form):
    your_email = forms.EmailField(label='Your E-mail address', required=True)
    receive_email_updates_for_this_event = forms.ChoiceField(label='Do you wish to receive E-mail updates for this event?', choices=EMAIL_UPDATE_CHOICES, initial=False , required=False,  widget=forms.RadioSelect())
    name = forms.CharField(label='Your name', max_length=128,required=True)
    associated_organization = forms.CharField(label='Organization you are associated with', max_length=128,required=False)
    will_you_be_attending = forms.ChoiceField(label='Will you be attending?', widget=forms.RadioSelect(), choices=VISIBLE_ATTENDING_CHOICES,required=True, initial='yes')
    are_you_a_student = forms.ChoiceField(label='Are you a student?', widget=forms.RadioSelect(), choices=IS_STUDENT_CHOICE,required=True, initial='no')
    captcha_field_hidden = forms.CharField(widget=forms.HiddenInput(),required=False,initial='none')

    def clean_your_email(self):
    	data = self.cleaned_data['your_email']
    	is_email_valid = validate_email(self.cleaned_data['your_email'], check_mx=True, verify=True )
    	if not is_email_valid:
    		raise forms.ValidationError("This email address could not be verified!")
    	return data