'''
The information is stored in a dictionary and is used in the views.py file to render the information on the website.
'''

from django.db import models

class BasicInformation(models.Model):
    owner = models.CharField(max_length=100, default='wenwen', verbose_name='網站擁有者')
    title = models.CharField(max_length=100, verbose_name='網站標題')
    description = models.TextField(verbose_name='對於本網站的描述', blank=True, null=True)
    icon = models.ImageField(upload_to='images/icon/', verbose_name='網站icon', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = '網站基本資訊'
        verbose_name_plural = '網站基本資訊'

class SocialLink(models.Model):
    basic = models.ForeignKey(BasicInformation, on_delete=models.CASCADE, related_name='social_links', verbose_name='綁定網站基本資訊')
    CHOICES = (
        ('ti-facebook', 'Facebook'),
        ('ti-twitter', 'Twitter'),
        ('ti-instagram', 'Instagram'),
        ('ti-youtube', 'Youtube'),
        ('ti-linkedin', 'LinkedIn'),
        ('ti-pinterest', 'Pinterest'),
        ('ti-tumblr', 'Tumblr'),
        ('ti-google', 'Google'),
        ('ti-dribbble', 'Dribbble'),
        ('ti-github', 'GitHub'),
        ('ti-reddit', 'Reddit'),
        ('ti-skype', 'Skype'),
        ('ti-vimeo', 'Vimeo'),
        ('ti-flickr', 'Flickr'),
        ('ti-rss', 'RSS'),
    )
    name = models.CharField(max_length=50, choices=CHOICES, verbose_name='社群名稱')
    link = models.URLField(verbose_name='社群連結')

    def __str__(self):
        return self.get_name_display()
    
    class Meta:
        verbose_name = '社群連結'
        verbose_name_plural = '社群連結'

class ContactInformation(models.Model):
    basic = models.OneToOneField(BasicInformation, on_delete=models.CASCADE, related_name='contact_info', verbose_name='綁定網站基本資訊')
    address = models.CharField(max_length=100, verbose_name='地址')
    phone = models.CharField(max_length=20, verbose_name='電話')
    email = models.EmailField(verbose_name='電子郵件')

    def __str__(self):
        return self.basic.title + ' - ' + self.address
    
    class Meta:
        verbose_name = '聯絡資訊'
        verbose_name_plural = '聯絡資訊'