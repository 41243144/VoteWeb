# Generated by Django 5.1.7 on 2025-03-21 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_comment_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='studient_id',
        ),
    ]
