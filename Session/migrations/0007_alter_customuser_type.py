# Generated by Django 4.2.15 on 2024-12-03 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Session', '0006_alter_customuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Distributeur', 'Distributeur'), ('Agent', 'Agent'), ('Admin Régional', 'Admin Régional'), ('Admin Wilaya', 'Admin Wilaya'), ('Résponsable distributeur', 'Résponsable distributeur')], default='Agent', max_length=32),
        ),
    ]