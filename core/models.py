from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from batimart_pro import settings

class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='client_logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#007bff')
    secondary_color = models.CharField(max_length=7, default='#6c757d')
    font_family = models.CharField(max_length=100, default='Arial, sans-serif')
    plan = models.CharField(max_length=20, choices=[
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise')
    ])
    custom_domain = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.company_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name

class Page(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    is_home = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    meta_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('client', 'slug')

    def __str__(self):
        return f"{self.client.company_name} - {self.title}"

class Section(models.Model):
    page = models.ForeignKey(Page, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    order = models.IntegerField(default=0)
    section_type = models.CharField(max_length=50, choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('cta', 'Call to Action'),
    ])
    background_color = models.CharField(max_length=7, blank=True, null=True)
    background_image = models.ImageField(upload_to='section_backgrounds/', blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.page.title} - {self.title}"

class Menu(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.client.company_name} - {self.name}"

class Theme(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Default Theme')
    css = models.TextField()

    def __str__(self):
        return f"{self.client.company_name} - {self.name}"
    
class Testimonial(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.author} for {self.client.company_name}"
# core/models.py

from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"