from django import template
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q

register = template.Library()


@register.inclusion_tag("comments/list.html", takes_context=True)
def list_comments(context, sentinel_target_obj, head_label="Add a Comment"):
    if not hasattr(sentinel_target_obj, "comments"):
        raise ImproperlyConfigured

    if not hasattr(sentinel_target_obj, "add_comment_url"):
        raise ImproperlyConfigured

    criteria = {"is_public": True}
    if context["user"].is_authenticated:
        criteria |= {"author": context["user"]}
    or_condition = Q()
    for k, v in criteria.items():
        or_condition.add(Q(**{k: v}), Q.OR)

    return {
        "head_label": head_label,
        "user": context["user"],
        "comments": sentinel_target_obj.comments.filter(or_condition),
        "form_url": sentinel_target_obj.add_comment_url,
    }
