from django.contrib import admin
from models import Event
import uuid

class EventAdmin(admin.ModelAdmin):
    date_hiearchy = 'date_of_event'
    fieldsets = (
        (None, {
            'fields': ('title','date_of_event', 'slug', 'description','maximum_attendees'),
        }),
        ('Event Details', {
            'fields': ('hosted_by', 'street_address', 'city', 'state', 'zip_code', 'contact_email','telephone1','telephone2'),
        })
    )
    list_display = ('title', 'date_of_event')
    prepopulated_fields = {'slug': ('title','date_of_event')}
    search_fields = ('title', 'description', 'hosted_by')

admin.site.register(Event, EventAdmin)