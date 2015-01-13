# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from django.conf.urls import patterns, url
from vietskill.schedule import views

urlpatterns = patterns(
    '',
    url(r'^$', views.meeting_index, name='meeting'),
    url(r'^meeting/new', views.meeting_new, name='new_meeting'),
    url(r'^meeting/(?P<pk>[0-9]+)/delete/$', views.meeting_delete, name='delete_meeting'),
    url(r'^meeting/(?P<pk>[0-9]+)/update/$', views.meeting_update, name='update_meeting'),
    url(r'^meeting/', views.meeting_index, name='meeting'),

    url(r'^plan/new', views.plan_new, name='new_plan'),
    url(r'^plan/(?P<pk>[0-9]+)/update/$', views.plan_update, name='update_plan'),
    url(r'^plan/(?P<pk>[0-9]+)/delete/$', views.plan_delete, name='delete_plan'),
    url(r'^plan/', views.plan_index, name='plan'),

    url(r'^event/update', views.event_update_or_create, name='update_event'),
    url(r'^event/(?P<pk>[0-9]+)/delete/$', views.event_delete, name='delete_event'),
    url(r'^events/json$', views.event_json, name='fetch_events'),
    url(r'^event/', views.event_index, name='event'),

    url(r'^teaching_schedule/update', views.schedule_update_or_create, name='update_schedule'),
    url(r'^teaching_schedule/(?P<pk>[0-9]+)/delete/$', views.schedule_delete, name='delete_schedule'),
    url(r'^teaching_schedule/', views.schedule_index, name='teaching_schedule'),
)
