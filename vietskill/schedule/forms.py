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
import datetime

from django import forms
from vietskill import models

DT_FORMAT = "%m/%d/%Y_%H:%M"
D_FORMAT = "%m/%d/%Y"


class MeetingForm(forms.Form):
    """Custom form to process Meeting POST request
    """
    location = forms.CharField(label='Location', max_length=100)
    attendants = forms.CharField(label='Attendants')
    purpose = forms.CharField(label='Purpose')
    date = forms.CharField(label='Date')
    time = forms.CharField(label='Time')

    def clean(self):
        """Validate form data
        """
        date = self.cleaned_data.get('date')
        time = self.cleaned_data.get('time')
        dt_str = date + '_' + time
        dt = datetime.datetime.strptime(dt_str, DT_FORMAT)
        self.cleaned_data['datetime'] = dt

        return self.cleaned_data


class PlanForm(forms.Form):
    """Custom form to process Plan POST request
    """
    start_date = forms.CharField(label='Start date', max_length=100)
    due_date = forms.CharField(label='End date')
    content = forms.CharField(label='Content')
    status = forms.CharField(label='Status')
    staffs = forms.CharField(label='Time')

    def clean(self):
        """Validate form data
        """
        start_date_str = self.cleaned_data.get('start_date')
        due_date_str = self.cleaned_data.get('due_date')
        self.cleaned_data['start_date'] = datetime.datetime.strptime(start_date_str, D_FORMAT)
        self.cleaned_data['due_date'] = datetime.datetime.strptime(due_date_str, D_FORMAT)

        return self.cleaned_data


class EventForm(forms.Form):
    """Custom form to process Event POST request
    """
    id = forms.IntegerField(required=False)
    date = forms.CharField(label='Date')
    title = forms.CharField(label='Title')
    content = forms.CharField(label='Content')
    location = forms.CharField(label='Location')

    def clean(self):
        """Validate form data
        """
        miliseconds = self.cleaned_data.get('date')
        self.cleaned_data['date'] = datetime.datetime.fromtimestamp(float(miliseconds[:-3]))
        #import ipdb; ipdb.set_trace()
        event_id = self.cleaned_data.get('id')
        self.cleaned_data['id'] = event_id if event_id != 0 else None
        return self.cleaned_data


class ScheduleForm(forms.Form):
    """Custom form to process Schedule POST request
    """
    id = forms.IntegerField(required=False)
    staff = forms.CharField(label='Staff')
    day = forms.CharField(label='Day')
    session = forms.CharField(label='Session')
    subject = forms.CharField(label='Subject')
    classes = forms.CharField(label='Class')
    room = forms.CharField(label='Room')

    def clean(self):
        """Validate form data
        """
        return self.cleaned_data
