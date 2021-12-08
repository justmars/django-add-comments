# Frontend

## Load comment form in sentinel view

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

The loading of the `<div>` triggers a `GET` request to the `form_url` aka `obj.add_comment_url`. The response is swapped into the DOM, replacing `this` blank div with a rendered `<form></form>`, i.e. `CommentModelForm`.

No page refresh was done, courtesy of html-sent-over-the-wire.

## Comment added to the top of the sentinel view, without page refresh

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
                "comments/inserter.html", # see comments/templates/inserter.html
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
