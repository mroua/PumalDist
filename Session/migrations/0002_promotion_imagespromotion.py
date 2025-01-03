# Generated by Django 4.2.15 on 2024-12-26 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Session', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('titre', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImagesPromotion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.FileField(blank=True, null=True, upload_to='Promotions')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Session.promotion')),
            ],
        ),
    ]
