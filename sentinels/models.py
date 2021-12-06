from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from comments.models import AbstractCommentable


class Sentinel(AbstractCommentable):

    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("sentinels:sentinel_detail", kwargs={"pk": self.pk})

    @cached_property
    def add_comment_url(self) -> str:
        from .urls import app_name

        return reverse(f"{app_name}:hx_comment_adder", kwargs={"pk": self.pk})
