from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField(max_length=500)
    
    author = models.ForeignKey(
        to=User,
        related_name='posts',
        on_delete=models.CASCADE
    )
    
    like = models.ManyToManyField(to=User, related_name='likes', blank=True)
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
