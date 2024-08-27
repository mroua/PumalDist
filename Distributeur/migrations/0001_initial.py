# Generated by Django 4.2.15 on 2024-08-27 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Distributeur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, default='0000000', max_length=100, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('nif', models.CharField(blank=True, max_length=20, null=True)),
                ('nis', models.CharField(blank=True, max_length=20, null=True)),
                ('art', models.CharField(blank=True, max_length=20, null=True)),
                ('rc', models.CharField(blank=True, max_length=20, null=True)),
                ('plafonnement', models.FloatField(blank=True, default=1000000, null=True)),
                ('bloquer', models.BooleanField(default=False)),
                ('echeance_jour', models.IntegerField(blank=True, default=0, null=True)),
                ('ristourn_a', models.FloatField(default=0)),
                ('ristourn_na', models.FloatField(default=0)),
                ('objectif_a', models.FloatField(default=0)),
                ('objectif_m', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Payeur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(default='0000000', max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('telephone', models.CharField(blank=True, max_length=200, null=True)),
                ('adresse', models.CharField(blank=True, max_length=200, null=True)),
                ('active', models.BooleanField(default=True)),
                ('nif', models.CharField(blank=True, max_length=20, null=True)),
                ('nis', models.CharField(blank=True, max_length=20, null=True)),
                ('art', models.CharField(blank=True, max_length=20, null=True)),
                ('rc', models.CharField(blank=True, max_length=20, null=True)),
                ('date_ajout', models.DateTimeField(auto_now=True)),
                ('draft', models.BooleanField(default=False)),
                ('distributeur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Distributeur.distributeur')),
            ],
        ),
    ]
