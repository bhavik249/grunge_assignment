# Generated by Django 3.1.5 on 2022-11-13 17:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('grunge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='UUID')),
                ('name', models.CharField(help_text='The playlist name', max_length=100)),
                ('tracks', models.ManyToManyField(to='grunge.Track')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AddIndex(
            model_name='playlist',
            index=models.Index(fields=['name'], name='grunge_play_name_ed1809_idx'),
        ),
    ]
