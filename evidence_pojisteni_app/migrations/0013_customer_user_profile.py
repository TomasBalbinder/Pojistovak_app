# Generated by Django 5.0.2 on 2024-05-23 14:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evidence_pojisteni_app', '0012_remove_customer_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='evidence_pojisteni_app.userprofile'),
            preserve_default=False,
        ),
    ]
