from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Blog(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True)
    summary = models.TextField(blank=True, null=True, help_text='Short teaser shown in lists and previews (optional)')
    featured_image = models.ImageField(upload_to='featured_images/%Y/%m/%d', blank=True, null=True, help_text='Main image for the post (recommended 1200x630)')
    content = CKEditor5Field(config_name='default', verbose_name='Blog Content')
    status = models.CharField(max_length=9, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    published_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='blogs')
    likes = models.ManyToManyField('accounts.User')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("blog_detail", args=[self.slug])

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    commentor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    class Meta:
        ordering = ['-created_at']



