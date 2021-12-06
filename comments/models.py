import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel


class Comment(TimeStampedModel):
    """Each arbitrary with an Abstract model with a related Comment by an authenticated user `author`."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # main fields
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="comments"
    )

    # generic fk base
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-modified", "-created"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("comments:hx_view_comment", kwargs={"id": self.id})

    @classmethod
    def get_for_user(cls, id: uuid.UUID, user):
        """Simple permission checking"""
        comment = get_object_or_404(cls, id=id)
        if comment.author != user:
            raise PermissionDenied()
        return comment


class AbstractCommentable(models.Model):
    comments = GenericRelation(
        Comment, related_query_name="%(app_label)s_%(class)ss"
    )

    class Meta:
        abstract = True
