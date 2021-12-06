from django.urls import path
from django.views.generic import DetailView, ListView

from .models import Sentinel
from .views import hx_comment_adder

app_name = "sentinels"
urlpatterns = [
    path(
        "add_comment/target/<int:pk>",
        hx_comment_adder,
        name="hx_comment_adder",
    ),
    path(
        "detail/<int:pk>",
        DetailView.as_view(
            model=Sentinel, template_name="sentinel_detail.html"
        ),
        name="sentinel_detail",
    ),
    path(
        "",
        ListView.as_view(model=Sentinel, template_name="sentinel_list.html"),
        name="sentinel_list",
    ),
]
