from django.urls import path
from django.views.generic import DetailView, ListView

from .apps import SentinelsConfig
from .models import Sentinel, SentinelSlugged

sentinel_patterns = [
    Sentinel.add_comment_path,
    path(
        "detail/sentinel/<int:pk>",
        DetailView.as_view(model=Sentinel, template_name="sentinel_detail.html"),
        name="sentinel_detail",
    ),
]

sentinel_slugged_patterns = [
    SentinelSlugged.add_comment_path,
    path(
        "detail/sentinel_slugged/<slug:slug>",
        DetailView.as_view(model=SentinelSlugged, template_name="sentinel_detail.html"),
        name="sentinel_slugged_detail",
    ),
]

app_name = SentinelsConfig.name
urlpatterns = (
    sentinel_patterns
    + sentinel_slugged_patterns
    + [
        path(
            "",
            ListView.as_view(model=Sentinel, template_name="sentinel_list.html"),
            name="sentinel_list",
        ),
    ]
)
