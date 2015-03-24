from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt   
import views

handler404 = 'fosstr_rsvp.views.error404'
handler500 = 'fosstr_rsvp.views.error500'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rsvp/events/$', views.ShowEvents.as_view(), name='events'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/$', csrf_exempt(views.EventView.as_view()), name='rsvp_event'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/thanks/$', views.RsvpSuccess.as_view(),name='thanks'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/failed/$', views.RsvpFailed.as_view(), name='failed'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/deniedrsvp/$', views.RsvpDenied.as_view(), name='deniedrsvp'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/full/$', views.EventFull.as_view(), name='full'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/duplicate/$', views.DuplicateRsvp.as_view(), name='duplicate'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/past_event/$', views.EventPassed.as_view(), name='past_event'),
)
