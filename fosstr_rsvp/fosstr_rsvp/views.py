from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, Http404
from models import Event, Guest
from django.db.models import Q
from forms import RSVPForm
from django.views.generic import FormView
from django.views.generic.base import TemplateView

import utils
from validate_email_address import validate_email

class ShowEvents(TemplateView):
	template_name = 'fosstr_rsvp/show_events.html'

	def get_context_data(self, **kwargs):
		context = super(ShowEvents, self).get_context_data(**kwargs)
		events = Event.objects.all()
		context['events'] = events
		return context

class DuplicateRsvp(TemplateView):
	template_name = 'fosstr_rsvp/duplicate.html'

	def get_context_data(self, **kwargs):
		try:
			slug = self.kwargs['slug']
			event = get_object_or_404(Event, slug=slug)
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
			event = get_object_or_404(Event, slug=slug)
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
			event = get_object_or_404(Event, slug=slug)
			context = super(RsvpSuccess, self).get_context_data(**kwargs)
			context['event'] =  event
			return context
		except Exception,e:
			raise Http404()

class RsvpFailed(TemplateView):
	template_name = 'fosstr_rsvp/failed.html'

	def get_context_data(self, **kwargs):
		slug = self.kwargs['slug']
		event = get_object_or_404(Event, slug=slug)
		context = super(RsvpFailed, self).get_context_data(**kwargs)
		context['event'] =  event
		return context

class EventFull(TemplateView):
	template_name = 'fosstr_rsvp/full.html'

	def get_context_data(self, **kwargs):
		slug = self.kwargs['slug']
		event = get_object_or_404(Event, slug=slug)
		context = super(EventFull, self).get_context_data(**kwargs)
		context['event'] =  event
		return context

class EventView(FormView):
    template_name = 'fosstr_rsvp/event_view.html'
    form_class = RSVPForm

    def post(self, request, *args, **kwargs):
    	try:
    		slug = self.kwargs['slug']
    		event = get_object_or_404(Event, slug=slug)
    		guest_email = request.REQUEST['your_email']
    		guest_name = request.REQUEST['name']
    		guest_associated_organization = request.REQUEST['associated_organization']
    		guest_attending_status = request.REQUEST['will_you_be_attending']
    		guest_is_student = request.REQUEST['are_you_a_student']
    		is_guest_present = Guest.objects.filter(Q(email=guest_email))
    		rsvp_count = Guest.objects.count()
    		if rsvp_count >= event.maximum_attendees:
    			return HttpResponseRedirect('/rsvp/event/%s/full/' % slug)
    		is_email_valid = validate_email(guest_email, check_mx=True, verify=True)
    		print "Is email valid : ", is_email_valid
    		if not is_email_valid:
    			return HttpResponseRedirect('/rsvp/event/%s/failed/' % slug)
    		if is_guest_present:
    			return HttpResponseRedirect('/rsvp/event/%s/duplicate/' % slug )
    		if guest_attending_status.lower() == 'no':
    			return HttpResponseRedirect('/rsvp/event/%s/deniedrsvp/' % slug )
    		# g_recaptcha_response = request.REQUEST['g-recaptcha-response']
    		# guest_IP = utils.get_client_ip(request)
    		# priv_key = settings.RECAPTCHA_PRV_KEY
    		Guest.objects.create(event=event, email=guest_email, name=guest_name, attending_status=guest_attending_status,associated_organization=guest_associated_organization, is_student=guest_is_student)
    		return HttpResponseRedirect('/rsvp/event/%s/thanks/' % slug)
    	except Exception,f:
    		print "Exception: ",f
    		return HttpResponseRedirect('/rsvp/event/%s/failed/' % slug)

    def get_context_data(self, **kwargs):
    	slug = self.kwargs['slug']
    	event = get_object_or_404(Event, slug=slug)
        context = super(EventView, self).get_context_data(**kwargs)
        context['event'] =  event
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context
