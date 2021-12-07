# App configuraiton

## Ensure sentinel namespace

The `app_name` namespace can be set/found in the `Sentinel`'s urls.py:

```python
# sentinels/urls.py
from .views import SentinelListView

app_name = "sentinels" # this is the namespace
urlpatterns = [path("", SentinelListView.as_view(), name="sentinel_list"), ...]
```

Thus, the `namespace` / `app_name` becomes `sentinels` and can produce a URL via a reverse function:

```python
from django.urls import reverse
reverse("sentinels:sentinel_list") # results in the url that will call `SentinelListView.as_view()`
```

## Add sentinel properties depending on primary key

Copy and paste an attribute to the `Sentinel` model:

```python
# sentinels/models.py
from comments.models import AbstractCommentable
class Sentinel(AbstractCommentable): # with `id` UUID and `slug`
    ...
    @cached_property
    def add_comment_url(self) -> str:
        from .urls import app_name

        return self.set_add_comment_url(app_name, self.slug) # see slug

    @classmethod
    def add_comment_func(cls, request, slug: str) -> TemplateResponse: # see slug
        return cls.set_comment_form(request, cls.objects.get(slug=slug)) # see slug

    @classproperty
    def add_comment_path(cls) -> URLPattern:
        return cls.set_add_comment_path("<slug:slug>", cls.add_comment_func) # see slug
```

For model instances having the implicit integer `pk` as model identifier:

```python
class Sentinel(AbstractCommentable): # with pk
    ...
    @cached_property
    def add_comment_url(self) -> str:
        from .urls import app_name

        return self.set_add_comment_url(app_name, self.pk) # see pk

    @classmethod
    def add_comment_func(cls, request, pk: int) -> TemplateResponse: # see pk
        return cls.set_comment_form(request, cls.objects.get(pk=pk)) # see pk

    @classproperty
    def add_comment_path(cls) -> URLPattern:
        return cls.set_add_comment_path("<pk:int>", cls.add_comment_func) # see pk
```

Assuming a sentinel instance `obj`, the declared property will enable the use of `add_comment_url`.

### Add sentinel property to URL patterns

Add the created _view_ function to a _url_.

```python
# sentinels/urls.py
from .models import Sentinel

app_name = "sentinels"
url_patterns = [Sentinel.add_comment_path, ...]
```

With this done, the following route, `obj.add_comment_url` becomes operational.

## Sentinel instances will now have access to comment urls

See `obj.add_comment_url` as used in a [template tag](./comments/templatetags/comments.py).

The form that represents this "add comment" action / url will be loaded in every comment list:

```jinja
<!-- sentinels/templates/sentinel_detail.html -->
<h1>Title: {{ object.title }}</h1>
{% load comments %} <!-- see templatetags/comments.py -->
{% list_comments %}
```

## Repeat the process for other models

1. The procedure above was undertaken with respect to the `Sentinel` model.
2. For another Django app, let's say `articles` with an `Article` model, the same procedure can be followed.
