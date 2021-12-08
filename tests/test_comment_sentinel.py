from http import HTTPStatus

import pytest
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import URLPattern

from sentinels.models import Sentinel


@pytest.mark.django_db
def test_sentinel_instance_add_comment_url_exists(a_sentinel):
    assert Sentinel._comment_prefix == "add_comment/sentinel"
    assert hasattr(a_sentinel, "add_comment_url")
    assert a_sentinel.add_comment_url == f"/{Sentinel._comment_prefix}/1"


@pytest.mark.django_db
def test_sentinel_instance_add_comment_path_exists(a_sentinel):
    assert Sentinel._comment_label == "hx_add_comment_to_sentinel"
    assert hasattr(a_sentinel, "add_comment_path")
    assert isinstance(a_sentinel.add_comment_path, URLPattern)
    assert a_sentinel.add_comment_path.name == Sentinel._comment_label


@pytest.mark.django_db
def test_add_comment_anonymous_redirected(client, a_sentinel):
    response = client.get(a_sentinel.add_comment_url)
    assert isinstance(response, HttpResponseRedirect)
    assert HTTPStatus.FOUND == response.status_code


def test_add_comment_get_authenticated(client, a_commenter, a_sentinel):
    client.force_login(a_commenter)
    response = client.get(a_sentinel.add_comment_url)
    assert isinstance(response, TemplateResponse)
    assert HTTPStatus.OK == response.status_code
    assert "comments/form.html" == response.template_name


def test_add_comment_post_authenticated(rf, a_commenter, a_sentinel):
    test_text = "New content in lorem ipsum formatting"
    request = rf.post(a_sentinel.add_comment_url, data={"content": test_text})
    request.user = a_commenter
    response = Sentinel.add_comment_func(request, a_sentinel.pk)
    assert isinstance(response, TemplateResponse)
    assert HTTPStatus.OK == response.status_code
    assert "comments/inserter.html" == response.template_name
    assert test_text in response.context_data["inserted"].content


@pytest.mark.django_db
def test_sentinel_detail_page_text_contains_comment_content(
    client, a_sentinel, a_comment
):
    x = bytes(a_comment.content, encoding="raw_unicode_escape")
    url = a_sentinel.get_absolute_url()
    response = client.get(url)
    assert isinstance(response, HttpResponse)
    assert HTTPStatus.OK == response.status_code
    assert x in response.content
