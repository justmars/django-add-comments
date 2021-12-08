from django import template
from django.core.exceptions import ImproperlyConfigured

register = template.Library()


@register.inclusion_tag("comments/list.html", takes_context=True)
def list_comments(context, sentinel_target_obj):

    if not hasattr(sentinel_target_obj, "comments"):
        raise ImproperlyConfigured

    if not hasattr(sentinel_target_obj, "add_comment_url"):
        raise ImproperlyConfigured

    return {
        "user": context["user"],
        "comments": sentinel_target_obj.comments.all(),
        "form_url": sentinel_target_obj.add_comment_url,
    }
