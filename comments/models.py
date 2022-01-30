import uuid
from typing import Callable, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import models
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.urls.resolvers import URLPattern
from django.utils.functional import classproperty
from django_extensions.db.models import TimeStampedModel


class Comment(TimeStampedModel):
    """The `AbstractCommentable` model has a comments field which map to this model."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    # main fields
    content = models.TextField()
    is_public = models.BooleanField(default=False)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.PROTECT, related_name="comments"
    )

    # generic fk base, uses CharField to accomodate sentinel models with UUID as primary key
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)  #
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

    @classproperty
    def _comment_label(cls) -> str:
        return f"add_comment_{cls._meta.model_name}"

    @classmethod
    def set_add_comment_url(cls, idx) -> str:
        """An `add_comment_url` needs to be initialized by all models inheriting from `AbstractCommentable`. This function generates a named route. The route originates from `set_add_comment_path`, which is added by the inheriting model to its URL patterns.

        Args:
            idx ([type]): This can either be the inheriting model instance's `slug` or `pk`, depending on the model's structure.

        Returns:
            str: a URL which will lead to to an `idx` instance. Calling this URL will enable the commenting function under `allow_commenting_form_on_target_instance()` to work.
        """
        return reverse(
            f"{cls._meta.app_label}:{cls._comment_label}", args=[idx]
        )

    @classmethod
    def set_add_comment_path(
        cls, endpoint_token: str, func_comment: Callable
    ) -> URLPattern:
        """The resulting path needs to be added to `urlpatterns`.

        Args:
            endpoint_token (str): e.g. <pk:int> or <title_slug:slug>, a converter URL parameter based on path converters
            func_comment (Callable): function call results in a TemplateResponse

        Returns:
            URLPattern: Should be added to `urlpatterns` list of `app_name`, inheriting child of AbstractCommentable.
        """
        return path(
            f"{cls._comment_label}/{endpoint_token}",
            func_comment,
            name=cls._comment_label,
        )

    @classmethod
    def allow_commenting_form_on_target_instance(
        cls, request: HttpRequest, target_obj: ContentType
    ) -> Union[TemplateResponse, HttpResponseRedirect]:
        """This cannot be determined without a declaration of the inheriting model. After the `target_obj` is determined, the signature will be complete for `func_comment` in `set_add_comment_path()`.

        Args:
            request (HttpRequest): Can be either GET or POST methods.
            target_obj (ContentType): The model instance being commented on.

        Returns:
            Union[TemplateResponse, HttpResponseRedirect]: If the user is not logged in, redirect via `HttpResponseRedirect`. Otherwise enable get/post requests resulting in a `TemplateResponse`.
        """
        from .forms import CommentModelForm

        if not request.user.is_authenticated:  # required to comment
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

        form = CommentModelForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.content_object = target_obj
            comment.save()
            context = {"inserted": comment, "form_url": request.path}
            return TemplateResponse(request, "comments/inserter.html", context)
        return TemplateResponse(request, "comments/form.html", {"form": form})
