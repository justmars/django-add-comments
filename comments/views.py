import uuid
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from .forms import InputCommentModelForm
from .models import Comment

CARD = "comment/card.html"


def hx_view_comment(request: HttpRequest, id: uuid.UUID) -> TemplateResponse:
    comment = get_object_or_404(Comment, id=id)
    return TemplateResponse(request, CARD, {"comment": comment})


@login_required
def hx_toggle_comment(request: HttpRequest, id: uuid.UUID) -> TemplateResponse:
    comment = Comment.get_for_user(id, request.user)
    comment.is_public = False if comment.is_public else True
    comment.save(update_fields=["is_public"])
    return TemplateResponse(request, CARD, {"comment": comment})


@login_required
@require_http_methods(["DELETE"])
def hx_del_comment(request: HttpRequest, id: uuid.UUID) -> HttpResponse:
    comment = Comment.get_for_user(id, request.user)
    comment.delete()
    return HttpResponse(status=200, headers={"HX-Trigger": "commentDeleted"})


@login_required
def hx_edit_comment(request: HttpRequest, id: uuid.UUID) -> TemplateResponse:
    """If a `form` is passed to the card, the update view is called; otherwse the comment's detail view is displayed."""
    comment = Comment.get_for_user(id, request.user)
    form = InputCommentModelForm(
        request.POST or None,
        instance=comment,
        submit_url=request.path,
        revert_url=comment.get_absolute_url(),
    )
    if request.method == "POST" and form.is_valid():
        comment.save(update_fields=["content", "is_public"])
        return TemplateResponse(request, CARD, {"comment": comment})
    return TemplateResponse(request, CARD, {"form": form, "comment": comment})


@login_required
def hx_add_comment_to_target_obj(
    request: HttpRequest, target_obj: ContentType
) -> Optional[TemplateResponse]:
    """This view should be inherited by a sentinel `target_obj`, which is the obj instance being commented on."""
    form = InputCommentModelForm(request.POST or None, submit_url=request.path)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.content_object = target_obj
        comment.save()
        context = {"inserted": comment, "form_url": request.path}
        return TemplateResponse(request, "comment/inserter.html", context)
    return TemplateResponse(request, "comment/form.html", {"form": form})
