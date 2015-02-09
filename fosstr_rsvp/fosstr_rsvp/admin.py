from django.contrib import admin
from models import Event


class EventAdmin(admin.ModelAdmin):
    date_hiearchy = 'date_of_event'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'date_of_event'),
        }),
        ('Event Details', {
            'fields': ('hosted_by', 'street_address', 'city', 'state', 'zip_code', 'contact_email'),
        })
    )
    list_display = ('title', 'date_of_event')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'hosted_by')

admin.site.register(Event, EventAdmin)