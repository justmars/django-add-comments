from http import HTTPStatus

import pytest
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse

from comments.views import CARD

ENDPOINT = lambda x: f"/comments/edit/{x}"
ROUTE = lambda x: reverse("comments:hx_edit_comment", kwargs={"id": x})


@pytest.mark.django_db
@pytest.mark.parametrize("formatter", [ENDPOINT, ROUTE])
def test_edit_comment_anonymous_redirected(client, a_comment, formatter):
    url = formatter(a_comment.id)
    response = client.get(url)
    assert isinstance(response, HttpResponseRedirect)
    assert HTTPStatus.FOUND == response.status_code


@pytest.mark.parametrize("formatter", [ENDPOINT, ROUTE])
def test_edit_comment_forbidden_even_if_authenticated(
    client, another_commenter, a_comment, formatter
):
    client.force_login(another_commenter)
    url = formatter(a_comment.id)
    client.get(url)
    with pytest.raises(PermissionDenied):
        raise PermissionDenied


@pytest.mark.parametrize("formatter", [ENDPOINT, ROUTE])
def test_edit_comment_get_authenticated(
    client, a_commenter, a_comment, formatter
):
    client.force_login(a_commenter)
    url = formatter(a_comment.id)
    response = client.get(url)
    assert isinstance(response, TemplateResponse)
    assert HTTPStatus.OK == response.status_code
    assert CARD == response.template_name


@pytest.mark.django_db
@pytest.mark.parametrize("formatter", [ENDPOINT, ROUTE])
def test_edit_comment_post_authenticated(
    client, modified_data, a_commenter, a_comment, formatter
):
    url = formatter(a_comment.id)
    client.force_login(a_commenter)
    response = client.post(url, data=modified_data)
    assert isinstance(response, TemplateResponse)
    assert HTTPStatus.OK == response.status_code
    assert CARD == response.template_name
