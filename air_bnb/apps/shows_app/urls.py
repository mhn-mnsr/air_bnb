from django.conf.urls import url
from django.contrib import admin
from . import views
  
urlpatterns = [
    
        url(r'^$', views.venues),
        url(r'^venues/(?P<venue_id>\d+)$', views.venue_profile),
        # need to add a show id to the end of the join url
        url(r'^add_show$', views.add_show),
        url(r'^delete_show/(?P<show_id>\d+)$', views.delete_show),
        url(r'^join/(?P<show_id>\d+)$', views.join_show),
        url(r'^band_submission$', views.band_submission),
  ]