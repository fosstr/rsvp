from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from models import Event, Guest
from django.db.models import Q
from forms import RSVPForm
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone

import utils

from django.shortcuts import render

def error404(request):
    return render(request,'fosstr_rsvp/404.html')

def error500(request):
    return render(request,'fosstr_rsvp/500.html')


class ShowEvents(TemplateView):
	template_name = 'fosstr_rsvp/show_events.html'

	def get_context_data(self, **kwargs):
		context = super(ShowEvents, self).get_context_data(**kwargs)
		events = Event.objects.filter(Q(date_of_event__gte = timezone.now()))
		past_events = Event.objects.filter(Q(date_of_event__lte = timezone.now()))
		context['events'] = events
		context['past_events'] = past_events
		return context

class DuplicateRsvp(TemplateView):
	template_name = 'fosstr_rsvp/duplicate.html'

	def get_context_data(self, **kwargs):
		try:
			slug = self.kwargs['slug']
			event = get_object_or_404(Event, slug=slug )
			context = super(DuplicateRsvp, self).get_context_data(**kwargs)
			context['event'] =  event
			return context
		except Exception,e:
			raise Http404()

class RsvpDenied(TemplateView):
	template_name = 'fosstr_rsvp/deniedrsvp.html'

	def get_context_data(self, **kwargs):
		try:
			slug = self.kwargs['slug']
			event = get_object_or_404(Event, slug=slug )
			context = super(RsvpDenied, self).get_context_data(**kwargs)
			context['event'] =  event
			return context
		except Exception,e:
			raise Http404()

class RsvpSuccess(TemplateView):
	template_name = 'fosstr_rsvp/success.html'

	def get_context_data(self, **kwargs):
		try:
			slug = self.kwargs['slug']
			event = get_object_or_404(Event, slug=slug )
			context = super(RsvpSuccess, self).get_context_data(**kwargs)
			context['event'] =  event
			return context
		except Exception,e:
			raise Http404()

class RsvpFailed(TemplateView):
	template_name = 'fosstr_rsvp/failed.html'

	def get_context_data(self, **kwargs):
		slug = self.kwargs['slug']
		event = get_object_or_404(Event, slug=slug )
		context = super(RsvpFailed, self).get_context_data(**kwargs)
		context['event'] =  event
		return context

class EventPassed(TemplateView):
    template_name = 'fosstr_rsvp/passed.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        event = get_object_or_404(Event, slug=slug )
        context = super(EventPassed, self).get_context_data(**kwargs)
        context['event'] =  event
        return context

class EventFull(TemplateView):
	template_name = 'fosstr_rsvp/full.html'

	def get_context_data(self, **kwargs):
		slug = self.kwargs['slug']
		event = get_object_or_404(Event, slug=slug )
		context = super(EventFull, self).get_context_data(**kwargs)
		context['event'] =  event
		return context

class EventView(FormView):
    template_name = 'fosstr_rsvp/event_view.html'
    form_class = RSVPForm

    def post(self, request, *args, **kwargs):
    	try:
    		slug = self.kwargs['slug']
    		rsvp_form = RSVPForm(request.POST)
    		event = get_object_or_404(Event, slug=slug )

    		if not rsvp_form.is_valid():
    			# THis is so that we maintain state
    			# The previous filled form is not lost
    			variables = {'form': rsvp_form, 'event': event }
    			return render(request, self.template_name, variables )

    		# Validate the CAPTCHA
    		try:
    			captcha_resp = request.REQUEST['g-recaptcha-response']
    		except:
    			variables = {'form': rsvp_form, 'event': event }
    			return render(request, self.template_name, variables )
    		remote_ip = utils.get_client_ip(request)
    		captcha_validity = utils.validateCaptcha(captcha_resp, remote_ip)
    		if not captcha_validity:
    			rsvp_form.add_error('captcha_field_hidden',"reCAPTCHA is not complete or incorrect. Complete the CAPTCHA to proceed")
    			variables = {'form': rsvp_form, 'event': event }
    			return render(request, self.template_name, variables )

    		# Pulling out values from the request
    		guest_email = request.REQUEST['your_email']
    		guest_name = request.REQUEST['name']
    		guest_associated_organization = request.REQUEST['associated_organization']
    		guest_attending_status = request.REQUEST['will_you_be_attending']
    		guest_is_student = request.REQUEST['are_you_a_student']
    		guest_wants_updates = False

    		# We have to do this since the field is a Boolean check box.
    		# Not clicking true is going to not return anything
    		if request.REQUEST.has_key('receive_email_updates_for_this_event'):
    			guest_wants_updates = request.REQUEST['receive_email_updates_for_this_event']

    		# Getting current RSVP count  so that we are not above limit
    		rsvp_count = Guest.objects.filter(Q(attending_status='yes') & Q(event_id=event.id)).count()
    		if rsvp_count >= event.maximum_attendees:
    			return HttpResponseRedirect('/rsvp/event/%s/full/' % slug )

    		# Checking if this email ID has been used to RSVP before
    		is_guest_present = Guest.objects.filter(Q(email=guest_email) & Q(event_id=event.id))
    		if is_guest_present:
    			return HttpResponseRedirect('/rsvp/event/%s/duplicate/' % slug )

    		Guest.objects.create(event=event, email=guest_email, name=guest_name, attending_status=guest_attending_status,associated_organization=guest_associated_organization, is_student=guest_is_student, wants_updates= guest_wants_updates)
    		# If denied RSVP
    		if guest_attending_status.lower() == 'no':
    			return HttpResponseRedirect('/rsvp/event/%s/deniedrsvp/' % slug )
    		# Accept RSVP. 
    		if guest_wants_updates:
    			venue_info = [event.hosted_by, event.street_address, event.city, event.state ]
    			utils.sendConfirmationEmail(guest_email, guest_name, event.title, event.description, event.date_of_event, venue_info, event.speaker)
    		return HttpResponseRedirect('/rsvp/event/%s/thanks/' % slug )
    	except Exception, exp:
    		print "Exception: ",exp
    		return HttpResponseRedirect('/rsvp/event/%s/failed/' % slug )

    def get_context_data(self, **kwargs):
    	slug = self.kwargs['slug']
    	event = get_object_or_404(Event, slug=slug )
        context = super(EventView, self).get_context_data(**kwargs)
        if event.date_of_event <= timezone.now():
            self.template_name = 'fosstr_rsvp/passed.html'
        context['event'] =  event
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context
