from http import HTTPStatus

import pytest
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.urls import reverse


def ENDPOINT(x):
    return f"/comments/delete/{x}"


def ROUTE(x):
    return reverse("comments:hx_del_comment", kwargs={"id": x})


@pytest.mark.django_db
@pytest.mark.parametrize("formatter", [ENDPOINT, ROUTE])
def test_del_comment_anonymous_redirected(client, a_comment, formatter):
    url = formatter(a_comment.id)
    response = client.delete(url)
    assert isinstance(response, HttpResponseRedirect)
    assert HTTPStatus.FOUND == response.status_code


@pytest.mark.parametrize("formatter", [ENDPOINT, ROUTE])
def test_del_comment_forbidden_even_if_authenticated(
    client, another_commenter, a_comment, formatter
):
    url = formatter(a_comment.id)
    client.force_login(another_commenter)
    client.delete(url)
    with pytest.raises(PermissionDenied):
        raise PermissionDenied


@pytest.mark.parametrize("formatter", [ENDPOINT, ROUTE])
def test_del_comment_authenticated(client, a_commenter, a_comment, formatter):
    url = formatter(a_comment.id)
    client.force_login(a_commenter)
    response = client.delete(url)
    assert response.status_code == HTTPStatus.OK
    assert response.headers["HX-Trigger"] == "commentDeleted"
