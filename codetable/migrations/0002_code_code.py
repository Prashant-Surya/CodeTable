# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codetable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='code',
            field=models.CharField(default=' ', max_length=20000),
            preserve_default=False,
        ),
    ]
