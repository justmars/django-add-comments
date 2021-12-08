from http import HTTPStatus

import pytest
from django.template.response import TemplateResponse
from django.urls import reverse

from comments.views import CARD


@pytest.fixture
def test_view_comment_endpoint(client, a_comment):
    response = client.get(f"/comments/view/{a_comment.id}")
    assert isinstance(response, TemplateResponse)
    assert response.status_code == HTTPStatus.OK
    assert response.template_name == CARD


@pytest.fixture
def test_view_comment_route(client, a_comment):
    url = reverse("comments:hx_view_comment", kwargs={"id": a_comment.id})
    response = client.get(url)
    assert isinstance(response, TemplateResponse)
    assert response.status_code == HTTPStatus.OK
    assert response.template_name == CARD
