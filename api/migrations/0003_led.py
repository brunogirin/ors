# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_debug_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Led',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('colour', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('flash', models.IntegerField(choices=[(1, 1), (2, 2), (4, 4), (8, 8), (16, 16)])),
            ],
        ),
    ]
