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
    def uniform_add_comment_label(cls) -> str:
        """Creates a default name (and the prefix of the endpoint) for the prospective `add_comment_path`."""
        return f"hx_add_comment_to_{cls._meta.model_name}"

    @classmethod
    def set_add_comment_url(cls, app_name: str, identifier) -> str:
        """An `add_comment_url` needs to be declared by all models that inherit from `AbstractCommentable`. Ths will generate a named_route to be used in URL patterns based on the model name. If the model name is `Entry`, the `commenting_func_name` will be `hx_add_comment_to_entry`. This string will then be added to the app name, and the instance id, to form the full route."""
        named_route = f"{app_name}:{cls.uniform_add_comment_label}"
        return reverse(named_route, args=[identifier])  # can be pk or slug

    @classmethod
    def set_add_comment_path(
        cls, url_endpoint: str, comment_form_processor: Callable
    ) -> URLPattern:
        """An `add_comment_url` needs to be declared by all models that inherit from `AbstractCommentable`. Ths will generate a named_route to be used in URL patterns based on the model name. If the model name is `Entry`, the `commenting_func_name` will be `hx_add_comment_to_entry`. This string will then be added to the app name, and the instance id, to form the full route."""
        route = f"{cls.uniform_add_comment_label}/{url_endpoint}"
        name = cls.uniform_add_comment_label
        return path(route, comment_form_processor, name=name)

    @classmethod
    def set_comment_form(
        cls, request: HttpRequest, target_obj: models.Model
    ) -> Union[TemplateResponse, HttpResponseRedirect]:
        """Will create function callable in the inheriting `app_name`'s `urlpatterns` list. This view should be inherited by a sentinel `target_obj`, which is the obj instance being commented on."""
        from .forms import InputCommentModelForm

        if not request.user.is_authenticated:
            # only logged in users can post a comment
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))

        form = InputCommentModelForm(
            request.POST or None,
            submit_url=request.path,
        )
        if request.method == "POST" and form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.content_object = target_obj
            comment.save()
            return TemplateResponse(
                request,
                "comment/inserter.html",
                {"inserted": comment, "form_url": request.path},
            )
        return TemplateResponse(request, "comment/form.html", {"form": form})
