# Generated by Django 3.0.6 on 2020-07-18 17:36

from django.db import migrations, models
import django.db.models.deletion
import memories.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, default='No description provided', max_length=1500)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=memories.models.file_upload_path)),
                ('name', models.CharField(blank=True, default='', max_length=155)),
                ('memory', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='memories.Memory')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Profile')),
            ],
        ),
    ]
