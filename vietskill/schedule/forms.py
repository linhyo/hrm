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

