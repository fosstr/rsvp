# RSVP

This is the RSVP app being used by [FOSSTR](http://fosstr.org/)

The app has been heavily influenced by [bitmazk/django-event-rsvp](https://github.com/bitmazk/django-event-rsvp) and [toastdriven/django-rsvp](https://github.com/toastdriven/django-rsvp) but has been simplified and tuned for our needs

Feel free to use, improve and send us a pull request

\- Team FOSSTR

-------------
Getting Started
-------------

It is recommended to run this app inside a virtual environment

To install `virtualenv` through `pip`

`$ pip install virtualenv`

Once installed. Clone the repository

`$ git clone https://github.com/fosstr/rsvp.git`

Enter the working dir and create a virtual environment

`$ virtualenv .venv`

and activate it by

`$ source .venv/bin/activate`

Install the requirements using `pip` as 

`$ pip install -r requirements.txt`

Users will also have to setup a [reCAPTCHA](http://www.google.com/recaptcha/intro/index.html) account and store the Private key and Site key as the `RECAPTCHA_PRV_KEY` and the `RECAPTCHA_SITE_KEY` environment variables respectively

You have everything needed to run the app.

Make sure the models are inline with the DB Schema

`$ python manage.py syncdb`

Run the local django webserver using 

`$ python manage.py runserver`

If you install any other packages, add them to requirements.txt using 

`$ pip freeze > requirements.txt`


-------------
Settings
-------------

The following variables need to be defined in the shell environment from which the Python instances that launches django is present

RECAPTCHA_PRV_KEY -  The private key for the reCAPTCHA service

RECAPTCHA_SITE_KEY -  The Site key for the reCAPTCHA service

RSVP_EMAIL_USER - Email address to use for sending RSVP confirmations and reminders

RSVP_EMAIL_PASS - Password for the above account

Also additionally, You will have to add the correct key into event_view.html for reCAPTCHA

