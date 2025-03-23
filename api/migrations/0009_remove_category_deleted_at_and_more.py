# Generated by Django 5.1.7 on 2025-03-19 12:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_profile_created_at_alter_profile_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='deleted_at',
        ),
        migrations.AlterField(
            model_name='category',
            name='create_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_create_user', to=settings.AUTH_USER_MODEL, verbose_name='建立者'),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='建立時間'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, verbose_name='類別名稱'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新時間'),
        ),
    ]
