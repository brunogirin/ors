# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_led'),
    ]

    operations = [
        migrations.CreateModel(
            name='HouseCode',
            fields=[
                ('code', models.CharField(max_length=50, serialize=False, primary_key=True)),
            ],
        ),
    ]
