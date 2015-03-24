from django_cron import CronJobBase, Schedule
from django.utils import timezone
from django.db.models import Q
from django.utils import timezone

from models import Event, Guest

import utils

class WeeklyReminderCron(CronJobBase):
	code = 'weekly_reminder_cron'
	schedule = Schedule(run_at_times=['18:00'])

	def do(self):
		# Send reminder email to all guests who
		# have subscribed for Email Updates
		guest_list = []

		delta_start_date = timezone.now()
		delta_end_date = timezonne.now() + datetime.timedelta(hours=24)

		events_in_next_24_hours = Event.objects.filter( Q( date_of_event__range = [ delta_start_date, delta_end_date] ) ).distinct()
		for event in events_in_next_24_hours:
			guests = Guest.objects.filter(Q(event_id = event.id) & Q(wants_updates = True )).distinct()
			venue_info = [event.hosted_by, event.street_address, event.city, event.state ]
			for guest in guests:
				guest_list.append(guest.name)
				utils.sendReminderEmail( guest.name,guest.email,venue_info, event.title, event.description, event.speaker, event.date_of_event )

			# Send update to mailing list about event
			# Include: All Guests, Event Details
			utils.sendSummaryToML(guest_list, venue_info, event.title, event.description, event.speaker, event.date_of_event )