from django.conf.urls import patterns, include, url
from django.contrib import admin
import views

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rsvp/events/$', views.ShowEvents.as_view(), name='events'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/$', views.EventView.as_view(), name='rsvp_event'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/thanks/$', views.RsvpSuccess.as_view(),name='thanks'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/failed/$', views.RsvpFailed.as_view(), name='failed'),
    url(r'^rsvp/event/(?P<slug>[A-Za-z0-9_-]+)/duplicate/$', views.DuplicateRsvp.as_view(), name='duplicate'),
)
