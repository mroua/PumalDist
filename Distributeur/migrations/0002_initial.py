# Generated by Django 4.2.15 on 2024-11-22 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Session', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Distributeur', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payeur',
            name='ville',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Session.ville'),
        ),
        migrations.AddField(
            model_name='distributeur',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AddField(
            model_name='distributeur',
            name='ville',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Session.ville'),
        ),
    ]
