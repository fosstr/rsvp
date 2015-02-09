import datetime
from django.db import models

ATTENDING_CHOICES = (
    ('yes', 'Yes'),
    ('no', 'No'),
    ('no_rsvp', 'Hasn\'t RSVPed yet')
)

IS_STUDENT_CHOICE = (
    ('yes', 'Yes'),
    ('no', 'No')
    )

class Event(models.Model):
    title = models.CharField(max_length=255)    
    slug = models.SlugField(help_text='Short label for the event, containing only letters, numbers, underscores or hyphens')
    description = models.TextField()
    date_of_event = models.DateTimeField()
    hosted_by = models.CharField(max_length=255, help_text='The name of the person/organization hosting the event.', blank=False, default='')
    street_address = models.CharField(max_length=255, help_text='The street address where the event is being held.', blank=False, default='')
    city = models.CharField(max_length=64, help_text='The city where the event is being held.', blank=False, default='')
    state = models.CharField(max_length=64, help_text='The state where the event is being held.', blank=False, default='')
    zip_code = models.CharField(max_length=10, help_text='The zip code where the event is being held.', blank=False, default='')
    contact_email = models.EmailField(blank=False, default='contact@fosstr.org',help_text='Email to contact incase of questions')
    created = models.DateTimeField(default=datetime.datetime.now)
    
class Guest(models.Model):
    event = models.ForeignKey(Event)
    email = models.EmailField(blank=False,help_text='Your email address, We will send you weekly updates of the meetup')
    name = models.CharField(max_length=128, blank=False, default='',help_text='Your name')
    associated_organization = models.CharField(max_length=64,blank=False,default='unknown',help_text='What organization are you associated with, This is for us to guage our audience')
    attending_status = models.CharField(max_length=32 ,default='no_rsvp')
    is_student = models.CharField(max_length=32, default='no')
    rsvp_time = models.DateTimeField(default=datetime.datetime.now)
