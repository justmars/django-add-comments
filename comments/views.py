import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from .forms import CommentModelForm
from .models import Comment

CARD = "comments/card.html"


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
    form = CommentModelForm(request.POST or None, instance=comment)
    if request.method == "POST" and form.is_valid():
        comment.save(update_fields=["content", "is_public"])
        return TemplateResponse(request, CARD, {"comment": comment})
    return TemplateResponse(request, CARD, {"form": form, "comment": comment})
