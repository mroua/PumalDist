# Generated by Django 4.2.15 on 2024-08-15 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Produits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesure',
            name='type',
            field=models.CharField(choices=[('Unité', 'Unité'), ('Sac', 'Sac')], default='Unité', max_length=12),
        ),
    ]
