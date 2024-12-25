# Generated by Django 4.2.15 on 2024-12-21 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Distributeur', '0002_initial'),
        ('Encaissement', '0004_remove_factures_fc_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='factures',
            name='payeur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Distributeur.payeur'),
        ),
    ]