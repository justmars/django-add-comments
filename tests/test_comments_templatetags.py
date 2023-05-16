import pytest
from django.template import Context, Template


@pytest.mark.django_db
def test_rendered(a_sentinel, a_comment, another_commenter):
    context = Context({"object": a_sentinel, "user": another_commenter})
    template_to_render = Template("""
        {% load comments %}
        {% list_comments object %}
        """)
    rendered_template = template_to_render.render(context)
    assert a_comment.content in rendered_template
