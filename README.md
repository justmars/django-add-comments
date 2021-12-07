# Comments

Enable basic commenting for an arbitrary Django model.

```python
# app_model/models.py
from comment.models import AbstractCommentable
class Sentinel(AbstractCommentable):
    """Any `app_model` e.g. `Essay`, `Article`, etc... can be "commentable". We'll use `Sentinel`, as a demo, to refer to an arbitrary model that will have its own `comments` field mapped to a generic `Comment` model because of inheriting from the `AbstractCommentable` mixin."""
    title = models.CharField(max_length=50)
```

The instances – e.g. `Sentinel` with _id=1_, `Sentinel` with _id=2_, etc. – will have their own related `Comment`s. `django-add-comments` also includes ability to:

1. View a list of existing comments on sentinel _id=1_
2. Adding a comment (if logged in) on sentinel _id=2_
3. Deleting a comment (if made by the `author` of such comment)
4. Updating an added comment's `content` (if made by an `author` of such comment)
5. Toggling visibility of the comment to the public (if made by an `author` of such comment).

## Quickstart

1. [Install](./comments/docs/setup.md) django-add-comments app
2. [Configure](./comments/docs/add_comments.md) target model's properties, urls, template
3. Once setup, can dive into understanding htmx-driven [frontend](./comments/docs/frontend.md).
4. The [procedure](./comments/docs/add_comments.md) described in the docs related to a hypothetical `Sentinel` model. For another Django app, let's say an `articles` app with an `Article` model, the same procedure can be followed.
