from django.urls import path

from .views import (
    hx_del_comment,
    hx_edit_comment,
    hx_toggle_comment,
    hx_view_comment,
)

app_name = "comments"
urlpatterns = [
    path("toggle/<uuid:id>", hx_toggle_comment, name="hx_toggle_comment"),
    path("edit/<uuid:id>", hx_edit_comment, name="hx_edit_comment"),
    path("delete/<uuid:id>", hx_del_comment, name="hx_del_comment"),
    path("view/<uuid:id>", hx_view_comment, name="hx_view_comment"),
]
