from django.db import models
from django.shortcuts import reverse


# from autoslug import AutoSlugField


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.tag

    def get_absolute_url(self) -> str:
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse('category', kwargs={'cat_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(default=0, blank=True)

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
    tags = models.ManyToManyField(TagPost, blank=True, related_name='womens')
    husband = models.OneToOneField(Husband, on_delete=models.SET_NULL, null=True, blank=True, related_name='wife')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('post', kwargs={'post_slug': self.slug})
