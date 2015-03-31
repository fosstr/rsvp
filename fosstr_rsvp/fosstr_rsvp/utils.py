#!/usr/bin/env python

import requests
import settings
import smtplib
import random

HELLO_GREETINGS = ['Hey','Hello','Howdy','Namaskara','Greetings','Hi','Bonjour','Welcome','Aloha']
CLOSING_REMARKS = ['Regards','Best','See you there','Cheers','Thanks']


def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
        else:
                ip = request.META.get('REMOTE_ADDR')
        return ip


def validateCaptcha(CAPTCHA_RESPONSE,REMOTE_IP=None):
	payload = {'secret': settings.RECAPTCHA_PRV_KEY , 'response': CAPTCHA_RESPONSE , 'remoteip': REMOTE_IP }
	if REMOTE_IP == None:
		payload = {'secret': settings.RECAPTCHA_PRV_KEY , 'response': CAPTCHA_RESPONSE  }
	resp_obj = requests.get(settings.RECAPTCHA_VERIFY_URL, params=payload )
	if resp_obj.status_code != 200:
		return False
	response = resp_obj.json()
	return response['success']


def sendConfirmationEmail(recipients_email, name, title, description, date_of_event, venue, speaker):
	recipients = [recipients_email]
	subject = "[RSVP Confirmation] Upcoming event - %s" % title
	venue_info = ", ".join(venue)
	content = """

%s %s, 

This is to confirm your RSVP to the aforementioned meetup

Title: %s
Speaker: %s
Description: %s
Date: %s
Venue: %s

If you wish to remove yourself from the RSVP please contact us

Hope to see you there!

Note: Please bring a laptop to have a hands on experience of the session

%s,

Team FOSSTR
http://www.fosstr.org

# This is an auto generated mail from RSVP@FOSSTR 
# You are being sent this email since you have clicked on 'Receive email updates' on the RSVP page
# FOSSTR Meets are free for anyone to attend. There are absolutely no fees or strings attached
# Just come with an open mind and willingness to share and learn

	""" % (random.choice(HELLO_GREETINGS), name, title, speaker ,description, date_of_event, venue_info ,random.choice(CLOSING_REMARKS))

	message = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n%s" %
	           (settings.EMAIL_SENDER, ", ".join(recipients), subject, content))

	try:
	    server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_SERVER_PORT)
	    server.ehlo()
	    server.starttls()
	    server.ehlo
	    server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
	    server.sendmail(settings.EMAIL_SENDER, recipients, message)
	except Exception, e:
	    print "Error: unable to send email ", e


def sendReminderEmail(guest_name, guest_email, venue, event_title, event_description, event_speaker, date_of_event ):
	recipients = [guest_email]
	subject = "[Reminder] Upcoming event - %s" % event_title
	venue_info = ", ".join(venue)
	content = """

%s %s, 

This email is to remind you of an upcoming meetup

Title: %s
Speaker: %s
Description: %s
Date: %s
Venue: %s

Note: Please bring a laptop to have a hands on experience of the session

%s,

Team FOSSTR
http://www.fosstr.org

# This is an auto generated mail from RSVP@FOSSTR 
# You are being sent this email since you have clicked on 'Receive email updates' on the RSVP page
# FOSSTR Meets are free for anyone to attend. There are absolutely no fees or strings attached
# Just come with an open mind and willingness to share and learn

	""" % (random.choice(HELLO_GREETINGS), guest_name, event_title, event_speaker , event_description, date_of_event, venue_info ,random.choice(CLOSING_REMARKS))

	message = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n%s" %
	           (settings.EMAIL_SENDER, ", ".join(recipients), subject, content))

	try:
	    server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_SERVER_PORT)
	    server.ehlo()
	    server.starttls()
	    server.ehlo
	    server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
	    server.sendmail(settings.EMAIL_SENDER, recipients, message)
	except Exception, e:
	    print "Error: unable to send email ", e

def sendSummaryToML(guest_list, venue, event_title, event_description, event_speaker, date_of_event ):
	recipients = [settings.MAILING_LIST_EMAIL,'fosstr@fosstr.org']
	guest_name = "Glorious Mailing list"
	subject = "[Summary] Upcoming event - %s" % event_title
	venue_info = ", ".join(venue)
	content = """

%s %s, 

This is the weekly summary of RSVP to the upcoming event

Title: %s
Speaker: %s
Description: %s
Date: %s
Venue: %s

We have the following confirmed guests for the event

%s

Note: Please bring a laptop to have a hands on experience of the session

%s,

Team FOSSTR
http://www.fosstr.org

# This is an auto generated mail from RSVP@FOSSTR 
# FOSSTR Meets are free for anyone to attend. There are absolutely no fees or strings attached
# Just come with an open mind and willingness to share and learn

	""" % (random.choice(HELLO_GREETINGS), guest_name, event_title, event_speaker , event_description, date_of_event, venue_info , "\n".join(guest_list) ,random.choice(CLOSING_REMARKS))

	message = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n%s" %
	           (settings.EMAIL_SENDER, ", ".join(recipients), subject, content))

	try:
	    server = smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_SERVER_PORT)
	    server.ehlo()
	    server.starttls()
	    server.ehlo
	    server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
	    server.sendmail(settings.EMAIL_SENDER, recipients, message)
	except Exception, e:
	    print "Error: unable to send email ", e
