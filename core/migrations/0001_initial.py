# Generated by Django 5.1.7 on 2025-03-17 06:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasicInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(default='wenwen', max_length=100, verbose_name='網站擁有者')),
                ('title', models.CharField(max_length=100, verbose_name='網站標題')),
                ('description', models.TextField(blank=True, null=True, verbose_name='對於本網站的描述')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='images/icon/', verbose_name='網站icon')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '網站基本資訊',
                'verbose_name_plural': '網站基本資訊',
            },
        ),
        migrations.CreateModel(
            name='ContactInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, verbose_name='地址')),
                ('phone', models.CharField(max_length=20, verbose_name='電話')),
                ('email', models.EmailField(max_length=254, verbose_name='電子郵件')),
                ('basic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_info', to='core.basicinformation', verbose_name='綁定網站基本資訊')),
            ],
            options={
                'verbose_name': '聯絡資訊',
                'verbose_name_plural': '聯絡資訊',
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('ti-facebook', 'Facebook'), ('ti-twitter', 'Twitter'), ('ti-instagram', 'Instagram'), ('ti-youtube', 'Youtube'), ('ti-linkedin', 'LinkedIn'), ('ti-pinterest', 'Pinterest'), ('ti-tumblr', 'Tumblr'), ('ti-google', 'Google'), ('ti-dribbble', 'Dribbble'), ('ti-github', 'GitHub'), ('ti-reddit', 'Reddit'), ('ti-skype', 'Skype'), ('ti-vimeo', 'Vimeo'), ('ti-flickr', 'Flickr'), ('ti-rss', 'RSS')], max_length=50, verbose_name='社群名稱')),
                ('link', models.URLField(verbose_name='社群連結')),
                ('basic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_links', to='core.basicinformation', verbose_name='綁定網站基本資訊')),
            ],
            options={
                'verbose_name': '社群連結',
                'verbose_name_plural': '社群連結',
            },
        ),
    ]
