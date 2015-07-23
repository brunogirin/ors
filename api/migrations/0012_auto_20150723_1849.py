# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20150723_1040'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Led',
        ),
        migrations.RemoveField(
            model_name='debug',
            name='state',
        ),
    ]
