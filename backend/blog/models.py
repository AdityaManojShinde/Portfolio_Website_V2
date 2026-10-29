
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

from blog.utils import blog_cover_upload_to


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:120].strip("-") or "category"
            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exclude(
                pk=self.pk
            ).exists():
                counter += 1
                suffix = f"-{counter}"
                slug = f"{base_slug[:120 - len(suffix)].rstrip('-')}{suffix}"

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(
        max_length=60,
        unique=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:60].strip("-") or "tag"
            slug = base_slug
            counter = 1

            while Tag.objects.filter(slug=slug).exclude(
                pk=self.pk
            ).exists():
                counter += 1
                suffix = f"-{counter}"
                slug = f"{base_slug[:60 - len(suffix)].rstrip('-')}{suffix}"

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    # Basic information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(max_length=300)

    # Content
    content = CKEditor5Field("Content", config_name="default")
    cover_image = models.ImageField(
        upload_to=blog_cover_upload_to,
        blank=True,
    )

    # Organization
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="blogs",
    )

    # Publishing
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # SEO
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "-published_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:200] or "blog"
            slug = base_slug
            counter = 1

            while Blog.objects.filter(slug=slug).exclude(
                pk=self.pk
            ).exists():
                counter += 1
                slug = f"{base_slug[:200]}-{counter}"

            self.slug = slug

        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
