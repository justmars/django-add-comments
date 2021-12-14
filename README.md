# django-add-comments

Add `comments` to a Django model via mixin:

```python
# app/models.py
from comment.models import AbstractCommentable # import mixin
class Sentinel(AbstractCommentable): # add to class declaration
    """Any `app`, e.g. `essay`, `article`... can be 'commentable'."""
    title = models.CharField(max_length=50)
```

| Action                | Authorization       | Description                          |
| --------------------- | ------------------- | ------------------------------------ |
| View comments list    | All users           | Add filter public/private later      |
| Get comment form      | Authenticated users | Reactive via htmx / hyperscript [^1] |
| Delete / edit comment | Authorized authors  | Reactive via htmx / hyperscript [^1] |

## Setup

### Load virtual env

```zsh
.venv> poetry add django-add-comments # pip3 install django-add-comments
```

Will include dependencies from [pyproject.toml](../../pyproject.toml):

```toml
python = "^3.8"
Django = "^4.0"
django-extensions = "^3.1.5"
django-crispy-forms = "^1.13.0"
```

### Add app to project settings

```python
# in project_folder/settings.py
INSTALLED_APPS = [
    ...,
    'crispy_forms',  # add crispy_forms at least > v1.13, if not yet added
    'comments' # this is the new django-comments folder
]
```

### Add basic routes to urlpatterns

```python
# in project_folder/urls.py
from django.urls import path, include # new
urlpatterns = [
    ...,
    path('comments/', include('comments.urls')) # routes for update, delete, view, toggle comment
]
```

### Add Comment model to database

```zsh
.venv> python manage.py migrate
```

## Configuration

### What we're going to do

```zsh
>>> obj = Sentinel.objects.create(title="A sample title") # instance is made, e.g. id=1, id=2, etc.
>>> obj.add_comment_url # url to add a comment to `A sample title`
```

A sentinel is the model being commented on.

We've created a dummy `Sentinel` model to represent this construct.

Let's say we've initialized one model instance called `obj` with `slug`="a-sample-title".

What we'd like is the ability to write a comment to `obj` through a url represented by: `obj.add_comment_url`

`@add_comment_url` thus needs to become a property of the `Sentinel` model.

### Add imports

```python
# sentinels/models.py
from comments.models import AbstractCommentable # new
from django.template.response import TemplateResponse # new
from django.urls import reverse, URLPattern # new
from django.utils.functional import cached_property, classproperty # new
```

### Make sentinel model inherit from abstract base model

```python
# sentinels/models.py
class Sentinel(AbstractCommentable): # new
    ...
```

### Add model properties

```python
# sentinels/models.py
class Sentinel(AbstractCommentable):

    id = models.UUIDField ... # identifier is UUID
    slug = models.Slugfield ...

    @cached_property # copy this to the sentinel model, note `slug` as identifier
    def add_comment_url(self) -> str:
        return self.set_add_comment_url(self.slug)

    @classmethod # copy this to the sentinel model, note `slug` as identifier
    def add_comment_func(cls, request, slug: str) -> TemplateResponse:
        target = cls.objects.get(slug=slug)
        return cls.allow_commenting_form_on_target_instance(request, target)

    @classproperty # copy this to the sentinel model, note `slug` as identifier
    def add_comment_path(cls) -> URLPattern:
        return cls.set_add_comment_path("<slug:slug>", cls.add_comment_func)
```

_Gotcha_: if `pk` is identifier, revise `<slug:slug>` to `<pk:int>` above:

1. `self.set_add_comment_url(app_name, self.pk)`
2. `def add_comment_func(cls, request, pk: int):`
3. `target = cls.objects.get(pk=pk)`
4. `cls.set_add_comment_path("<pk:int>", cls.add_comment_func)`

### Add sentinel namespaced url for adding comments

Add path to the sentinel's url patterns:

```python
# sentinels/urls.py
from .models import Sentinel
from .apps import SentinelConfig # already pre-made during `python manage.py startapp sentinels`
app_name = SentinelConfig.name # remember the `app_name` in relation to the `add_comment_url` property
url_patterns = [
    Sentinel.add_comment_path, # This is really just a shortcut to a created path.
    ...
]
```

### Add template tag for displaying comment form with list of added comments

Add template tag to sentinel's template to show form with list

```jinja
<!-- sentinels/templates/sentinel_detail.html -->
<h1>Title: {{ obj.title }}</h1>  <!-- the `obj` is whatever variable passed to the template -->
{% load comments %} <!-- see templatetags/comments.py which contains `object.add_comment_url`  -->
{% list_comments obj %}
```

The form that represents this "add comment" action / url will be loaded in every comment list. See context in [template tag](../templatetags/comments.py).

[^1]: [No page refresh](./comments/docs/frontend.md)
