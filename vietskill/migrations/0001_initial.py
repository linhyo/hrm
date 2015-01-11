# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('birthday', models.DateField()),
                ('sex', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('position', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=75)),
                ('address', models.CharField(max_length=128)),
                ('phone_number', models.CharField(max_length=11)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
