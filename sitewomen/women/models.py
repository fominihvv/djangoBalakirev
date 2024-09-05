from django.db import models
from django.shortcuts import reverse


# from autoslug import AutoSlugField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class Women(models.Model):
    class Meta:
        ordering = ['title', '-time_create']
        indexes = [
            models.Index(fields=['title', '-time_create']),
        ]

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    cat = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('post', kwargs={'post_slug': self.slug})
