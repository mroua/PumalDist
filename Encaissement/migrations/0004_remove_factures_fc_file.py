# Generated by Django 4.2.15 on 2024-12-10 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Encaissement', '0003_remove_factures_payeur_factures_bl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factures',
            name='fc_file',
        ),
    ]