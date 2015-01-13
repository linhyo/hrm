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
from django import template

register = template.Library()

@register.filter(name='mod')
def mod(value, mod_value):
    """Return mod value"""
    result = (value % mod_value) + 1
    return result

@register.filter(name='plan_status')
def plan_status(value):
    """Return status string based on status number
    """
    status = ['Done', 'Active', 'New']
    return status[int(value) - 1]


@register.filter(name='schedule_class')
def schedule_class(value):
    """Return schedule class based on item id
    """
    if value == None:
        return "blank_block"
    else:
        return "session" + str((value % 5) + 1)