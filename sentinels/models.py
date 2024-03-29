import uuid

from django.db import models
from django.template.response import TemplateResponse
from django.urls import URLPattern, reverse
from django.utils.functional import cached_property, classproperty
from django_extensions.db.fields import AutoSlugField

from comments.models import AbstractCommentable


class Sentinel(AbstractCommentable):
    """This is a test model. Uses an implicit int `pk`."""

    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(f"{self._meta.app_label}:sentinel_detail", args=[self.pk])

    @cached_property
    def add_comment_url(self) -> str:
        return self.set_add_comment_url(self.pk)

    @classmethod
    def add_comment_func(cls, request, pk: int) -> TemplateResponse:
        target = cls.objects.get(pk=pk)
        return cls.allow_commenting_form_on_target_instance(request, target)

    @classproperty
    def add_comment_path(cls) -> URLPattern:
        return cls.set_add_comment_path("<int:pk>", cls.add_comment_func)


class SentinelSlugged(AbstractCommentable):
    """This is a test model. Uses an explicit `uuid` as primary key,
    and a `slug` field for URLs."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    slug = AutoSlugField(populate_from=["title"])
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            f"{self._meta.app_label}:sentinel_slugged_detail", args=[self.slug]
        )

    @cached_property
    def add_comment_url(self) -> str:
        return self.set_add_comment_url(self.slug)

    @classmethod
    def add_comment_func(cls, request, slug: str) -> TemplateResponse:
        target = cls.objects.get(slug=slug)
        return cls.allow_commenting_form_on_target_instance(request, target)

    @classproperty
    def add_comment_path(cls) -> URLPattern:
        return cls.set_add_comment_path("<slug:slug>", cls.add_comment_func)
