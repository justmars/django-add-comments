from django import template

register = template.Library()


@register.inclusion_tag("comment/list.html", takes_context=True)
def list_comments(context):
    return {
        "user": context["user"],
        "comments": context["object"].comments.all(),
        "form_url": context["object"].add_comment_url,
    }
