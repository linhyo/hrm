# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vietskill', '0003_auto_20150109_0244'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='staffs',
            field=models.ManyToManyField(to='vietskill.StaffProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='meetingpaticipant',
            name='staff_id',
            field=models.IntegerField(default=-1, blank=True),
            preserve_default=True,
        ),
    ]
