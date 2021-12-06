from django.http import HttpRequest
from django.template.response import TemplateResponse

from comments.views import hx_add_comment_to_target_obj

from .models import Sentinel


def hx_comment_adder(request: HttpRequest, pk: int) -> TemplateResponse:
    obj = Sentinel.objects.get(pk=pk)
    return hx_add_comment_to_target_obj(request, obj)
