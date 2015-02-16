from django import forms
from models import ATTENDING_CHOICES, Guest, IS_STUDENT_CHOICE


VISIBLE_ATTENDING_CHOICES = [choice for choice in ATTENDING_CHOICES if choice[0] != 'no_rsvp']

class RSVPForm(forms.Form):
    your_email = forms.EmailField(required=True)
    receive_email_updates_for_this_event = forms.BooleanField(required=True, initial=True)
    name = forms.CharField(max_length=128,required=True)
    associated_organization = forms.CharField(max_length=128,required=False)
    will_you_be_attending = forms.ChoiceField(choices=VISIBLE_ATTENDING_CHOICES,required=True, initial='yes')
    are_you_a_student = forms.ChoiceField(choices=IS_STUDENT_CHOICE,required=True, initial='no')