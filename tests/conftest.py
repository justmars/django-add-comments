import pytest

from comments.models import Comment
from sentinels.models import Sentinel


@pytest.fixture
def a_commenter(django_user_model):
    return django_user_model.objects.create(
        username="userjohn", password="qwer1234qwer1234"
    )


@pytest.fixture
def another_commenter(django_user_model):
    return django_user_model.objects.create(
        username="intruderjuan", password="qwer1234qwer1234"
    )


@pytest.fixture
def a_sentinel():
    return Sentinel.objects.create(title="A sample title")


@pytest.fixture
def a_comment(a_sentinel, a_commenter):
    return Comment.objects.create(
        content="Lorem ipsum separate unique text",
        author=a_commenter,
        content_object=a_sentinel,
    )


@pytest.fixture
def sample_data():
    return {"content": "New title to be added!"}


@pytest.fixture
def modified_data(a_comment):
    """Implies existence of `a_comment` which will be modified"""
    return {"title": "Modified valid title"}
