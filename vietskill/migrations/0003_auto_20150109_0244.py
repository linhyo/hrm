# -*- coding: utf-8 -*-
"""Update Fields on Meeting & new table MeetingParticipant
"""
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('vietskill', '0002_assessment_event_meeting_plan_recruitment_staffshift_statistic_teachingschedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingPaticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=75)),
                ('phone', models.CharField(max_length=11)),
                ('staff_id', models.IntegerField(blank=True)),
                ('meeting', models.ForeignKey(to='vietskill.Meeting')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='date',
        ),
        migrations.RemoveField(
            model_name='meeting',
            name='time',
        ),
        migrations.AddField(
            model_name='meeting',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
            preserve_default=True,
        ),
    ]
