# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20150717_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='housecode',
            old_name='ds18b20_temperature',
            new_name='temperature_ds18b20',
        ),
    ]
