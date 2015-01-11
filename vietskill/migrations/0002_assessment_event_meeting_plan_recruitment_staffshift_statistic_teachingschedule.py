# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vietskill', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('assess_point', models.IntegerField()),
                ('staff', models.ForeignKey(to='vietskill.StaffProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('location', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=30)),
                ('purpose', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('note', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('due_date', models.DateField()),
                ('duration', models.IntegerField()),
                ('content', models.TextField()),
                ('status', models.CharField(max_length=1, choices=[(b'1', b'Completed'), (b'2', b'In Progress'), (b'3', b'New')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Recruitment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('release_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('office', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StaffShift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=30)),
                ('num_shift', models.IntegerField()),
                ('location', models.CharField(max_length=100)),
                ('staff', models.ForeignKey(to='vietskill.StaffProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_teaching_days', models.IntegerField()),
                ('days_off', models.IntegerField()),
                ('num_mistakes', models.IntegerField()),
                ('staff', models.ForeignKey(to='vietskill.StaffProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeachingSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=3, choices=[(b'Mon', b'Monday'), (b'Tue', b'Tuesday'), (b'Wed', b'Wednesday'), (b'Thu', b'Thursday'), (b'Fri', b'Friday'), (b'Sat', b'Saturday'), (b'Sun', b'Sunday')])),
                ('session', models.CharField(max_length=1, choices=[(b'1', b'7:15 - 9:00'), (b'2', b'9:30 - 11:15'), (b'3', b'12:30 - 14:15'), (b'4', b'14:45 - 16:30')])),
                ('subject', models.CharField(max_length=1, choices=[(b'1', b'Master of Ceremonies'), (b'2', b'Life Skill'), (b'3', b'Art'), (b'4', b'Soft Skill'), (b'5', b'Copy Editing'), (b'6', b'Communication'), (b'7', b'Culture'), (b'8', b'Marketing'), (b'9', b'Presentation')])),
                ('classes', models.CharField(max_length=20)),
                ('room', models.CharField(max_length=10)),
                ('staff', models.ForeignKey(to='vietskill.StaffProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
