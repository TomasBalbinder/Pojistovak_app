# Generated by Django 5.0.2 on 2024-05-17 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evidence_pojisteni_app', '0004_alter_insurance_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurance',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
