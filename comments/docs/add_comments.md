# Configure URL for adding comments

## What we're going to do

```zsh
>>> obj = Sentinel.objects.create(title="A sample title") # instance is made, e.g. id=1, id=2, etc.
>>> obj.add_comment_url # url to add a comment to `A sample title`
```

A sentinel is the model being commented on.

We've created a dummy `Sentinel` model to represent this construct.

Let's say we've initialized one model instance called `obj` with `slug`="a-sample-title".

What we'd like is the ability to write a comment to `obj` through a url represented by: `obj.add_comment_url`

`@add_comment_url` thus needs to become a property of the `Sentinel` model.

## Namespace as a prequisite

```python
# sentinels/urls.py
from .views import SentinelListView

app_name = "sentinels" # this is a namespace
urlpatterns = [path("", SentinelListView.as_view(), name="sentinel_list"), ...]

...
# see connection of `name` to `app_name` via reverse()
from django.urls import reverse
def sample_func():
    return reverse("sentinels:sentinel_list")

```

## What are the steps of configuration?

### sentinels/models.py

1. Add imports

   ```python
   # sentinels/models.py
   from comments.models import AbstractCommentable # new
   from django.template.response import TemplateResponse # new
   from django.urls import reverse, URLPattern # new
   from django.utils.functional import cached_property, classproperty # new
   ```

2. Add the mixin to the sentinel model

   Before:

   ```python
   # sentinels/models.py
   class Sentinel(models.Model):
       ...
   ```

   After:

   ```python
   # sentinels/models.py
   class Sentinel(AbstractCommentable): # new
       ...
   ```

3. Add properties to the sentinel model

   ```python
   # sentinels/models.py
   class Sentinel(AbstractCommentable):

       id = models.UUIDField ... # identifier is UUID
       slug = models.Slugfield ...

       @cached_property # copy this to the sentinel model, note `slug` as identifier
       def add_comment_url(self) -> str:
           from .urls import app_name

           return self.set_add_comment_url(app_name, self.slug)

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
   3. `target = cls.objects.get(pk=int)`
   4. `cls.set_add_comment_path("<pk:int>", cls.add_comment_func)`

### sentinels/urls.py

Add path to the sentinel's url patterns

```python
# sentinels/urls.py
from .models import Sentinel

app_name = "sentinels" # remember the app_name above in relation to the `add_comment_url` property
url_patterns = [
    Sentinel.add_comment_path, # This is really just a shortcut to a created "name route to a view" function.
    ...
]
```

### sentinels/templates/sentinel_detail.html

Add template tag to sentinel's template to show form with list

```jinja
<!-- sentinels/templates/sentinel_detail.html -->
<h1>Title: {{ sentinel_object.title }}</h1>
{% load comments %} <!-- see templatetags/comments.py which contains `object.add_comment_url`  -->
{% list_comments sentinel_object %} <!-- the `sentinel_object` is whatever variable passed to the template -->
```

The form that represents this "add comment" action / url will be loaded in every comment list. See context in [template tag](../templatetags/comments.py).
