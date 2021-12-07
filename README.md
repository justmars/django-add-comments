# Comments

Enable basic commenting for an arbitrary Django model by (a) adding an `AbstractCommentable` mixin and (b) configuring the properties and urls.

```python
from comments.models import AbstractCommentable

# app_model/models.py
class Sentinel(AbstractCommentable): # arbitrary app_model
    title = models.CharField(max_length=50)
    ...

# comments/models.py
class AbstractCommentable(models.Model):
    comments = GenericRelation(Comment) # comments connected to sentinel instance

    class Meta:
        abstract = True
```

## Quickstart

1. [Install](./comments/docs/setup.md) django-add-comments app
2. [Configure](./comments/docs/add_comments.md) target model's properties, urls, template]
3. Once setup, can dive into understanding htmx-driven [frontend](./comments/docs/frontend.md).

## Reusability

Any model e.g. `Essay`, `Article`, etc... and (not just `Sentinel`) can be "commentable". But for purposes of demonstration, we'll use "sentinel" to refer to the arbitrary model that will have its own `comments` field.

More specifically, the instances of such sentinel – e.g. Sentinel with _id=1_, Sentinel with _id=2_, etc. – need to have their own related comments. This means having the ability to:

1. View a list of existing comments on sentinel _id=1_
2. Adding a comment (if logged in) on sentinel _id=2_
3. Deleting a comment (if made by an `author`)
4. Updating an added comment's `content` (if made by an `author`)
5. Toggling visibility of the comment to the public.

All instances of the `Sentinel` model therefore will need their own commenting actions.

The [procedure](./comments/docs/add_comments.md) described in the docs related to a hypothetical `Sentinel` model. For another Django app, let's say an `articles` app with an `Article` model, the same procedure can be followed.
