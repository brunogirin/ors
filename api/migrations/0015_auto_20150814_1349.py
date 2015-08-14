# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_housecode_rad_open_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='housecode',
            name='light_colour',
            field=models.IntegerField(default=None, null=True, blank=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3)]),
        ),
        migrations.AddField(
            model_name='housecode',
            name='light_flash',
            field=models.IntegerField(default=None, null=True, blank=True, choices=[(1, 1), (2, 2), (3, 3)]),
        ),
        migrations.AddField(
            model_name='housecode',
            name='light_on_time',
            field=models.IntegerField(default=None, null=True, blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15)]),
        ),
    ]
