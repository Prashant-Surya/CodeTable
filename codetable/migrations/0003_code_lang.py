# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codetable', '0002_code_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='lang',
            field=models.CharField(default=b'C', max_length=20),
        ),
    ]
