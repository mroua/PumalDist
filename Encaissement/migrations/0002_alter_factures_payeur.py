# Generated by Django 4.2.15 on 2024-12-09 00:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Distributeur', '0002_initial'),
        ('Encaissement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factures',
            name='payeur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Distributeur.payeur'),
        ),
    ]
