# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vietskill', '0005_auto_20150112_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachingschedule',
            name='day',
            field=models.CharField(max_length=3, choices=[(b'1', b'Monday'), (b'2', b'Tuesday'), (b'3', b'Wednesday'), (b'4', b'Thursday'), (b'5', b'Friday'), (b'6', b'Saturday'), (b'7', b'Sunday')]),
            preserve_default=True,
        ),
    ]
