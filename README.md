# Comments

## Overview

Enable basic commenting functionality for an arbitrary Django model that contains an `AbstractCommentable` mixin class.

```python
from comments.models import AbstractCommentable

# sentinels/models.py
class Sentinel(AbstractCommentable): # arbitrary
    title = models.CharField(max_length=50)
    ...

# comments/models.py
class AbstractCommentable(models.Model): # generic foreign relationships to comments
    comments = GenericRelation(Comment, related_query_name="%(app_label)s_%(class)ss")

    class Meta:
        abstract = True
```

## Premises

Any model e.g. `Essay`, `Article`, etc... and (not just `Sentinel`) can be "commentable". But for purposes of demonstration, we'll use "sentinel" to refer to the arbitrary model that will have its own `comments` field.

More specifically, the instances of such sentinel – e.g. Sentinel with _id=1_, Sentinel with _id=2_, etc. – need to have their own related comments. This means having the ability to:

1. View a list of existing comments on sentinel _id=1_
2. Adding a comment (if logged in) on sentinel _id=2_
3. Deleting a comment (if made by an `author`)
4. Updating an added comment's `content` (if made by an `author`)
5. Toggling visibility of the comment to the public.

All instances of the `Sentinel` model therefore will need their own commenting actions. This app produces those actions through urls. See the following shell commands that show the desired url routes per sentinel instance:

```zsh
# instance is made, e.g. id=1, id=2, etc.
>>> obj = Sentinel.objects.create(title="A sample title")

# distinguish a `Sentinel` model with comments from an `Essay` model with comments using the app_name
>>> from sentinels.urls import app_name # required
>>> obj.add_comment_url # url to add a comment to `A sample title`
```

### Set sentinel namespace

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

### Add sentinel properties

Copy and paste an attribute to the `Sentinel` model:

```python
# sentinels/models.py
from comments.models import AbstractCommentable
class Sentinel(AbstractCommentable):
    ...
    @cached_property
    def add_comment_url(self) -> str:
        from .urls import app_name

        return reverse(f"{app_name}:hx_comment_adder", kwargs={"pk": self.pk})
```

Assuming a sentinel instance `obj`, the declared property will enable the use of `add_comment_url`.

### Add sentinel-comment views

Copy and paste the _view_:

```python
# sentinels/views.py
from comments.views import hx_add_comment_to_target_obj
from comments.models import Comment
from .models import Sentinel

def hx_comment_adder(request: HttpRequest, pk: int) -> TemplateResponse:
    obj = Sentinel.objects.get(pk=pk)
    return hx_add_comment_to_target_obj(request, obj)
```

### Add sentinel-comment urls

Add the created _view_ function to a _url_.

```python
# sentinels/urls.py
from .views import hx_comment_adder

app_name = "sentinels"
url_patterns = [path("add_coment/target/<int:pk>", hx_comment_adder, name="hx_comment_adder"), ...]
```

With this done, the following route, `obj.add_comment_url` becomes operational:

```python
from django.urls import reverse
reverse("sentinels:hx_comment_adder", kwargs={"pk":pk})
```

### Sentinel instances will now have access to comment urls

See `obj.add_comment_url` as used in a [template tag](./comments/templatetags/comments.py). The form that represents this "add comment" action / url will be loaded in every comment list:

```jinja
<!-- sentinels/templates/sentinel_detail.html -->
<h1>Title: {{ object.title }}</h1>
{% load comments %} <!-- see templatetags/comments.py -->
{% list_comments %}
```

### Load comment form in sentinel view

The basic view does not yet show a comment form.

When the `htmx`-ed `<div>` is loaded to the DOM, however, a few things happen because of the insertion of attributes in the `add_comment_template`:

```jinja
<!-- comments/templates/inserter.html -->
...
<section>
    <div hx-trigger="load" hx-get="{{form_url}}" hx-target="this" hx-swap="innerHTML">
    </div>
</section>
...

{% if inserted %}
    {% include './card.html' with comment=inserted %}
{% endif %}
```

The loading of the `<div>` triggers a `GET` request to the `form_url` aka `obj.add_comment_url`. The response is swapped into the DOM, replacing `this` blank div with a rendered `<form></form>`, i.e. `InputCommentModelForm`.

No page refresh was done, courtesy of html-sent-over-the-wire.

### Comment added to the top of the sentinel view, without page refresh

Note that in the above `inserter` template, an `inserted` variable is declared:

```jinja
...
{% if inserted %}
    {% include '../card.html' with comment=inserted %}
{% endif %}
```

When the fields of the instantiated form is populated and submitted, a `POST` request is sent to the same `hx_comment_adder` url.

The response targets the entire `<section>` because of the form's `<submit>` attributes declared via django-crispy-forms but it will replace the entire html fragment above because of swapping "outerHTML" (on the div) response from `POST`:

```python
# comments/forms.py
from crispy_forms.layout import Submit
...
Submit(
    "submit",
    "Submit",
    hx_post=submit_url, # i.e. `hx_comment_adder`
    hx_target=f"closest section", # see comments/templates/inserter.html
    hx_swap="outerHTML",
    hx_trigger="click",
)
# comments/views.py
from django.template.response import TemplateResponse
def hx_add_comment_to_target_obj(request: HttpRequest, target_obj: ContentType):
    ...
    if request.method == "POST" and form.is_valid():
        return TemplateResponse(
                request,
                "comment/inserter.html", # see comments/templates/inserter.html
                {
                    "inserted": comment, # newly inserted comment at the top of the list of comments
                    "form_url": request.path, # reloads the form because of hx-trigger "load"
                    "label": "Add Comment",
                },
            )
    ...
```

The `add_comment_template` is then reset:

1. The user can add a new comment since the form is replaced with an empty one;
2. The recently `inserted` comment is reflected at the top of the list of comments.
3. No page refresh is done, against courtesty of htmx.

### Repeat the process for other models

1. The procedure above was undertaken with respect to the `Sentinel` model.
2. For another Django app, let's say `articles` with an `Article` model, the same procedure can be followed.
