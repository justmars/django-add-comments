# Comments

Enable basic commenting functionality for an arbitrary Django model that contains an `AbstractCommentable` mixin class.

## Overview

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

Once setup, can dive into [understanding the frontend](./comments/docs/frontend.md) through the use of htmx and hyperscript.

## Quickstart

1. [Install app](./comments/docs/setup.md)
2. [Add generic comments to your model](./comments/docs/add_comments.md)

## Premises

Any model e.g. `Essay`, `Article`, etc... and (not just `Sentinel`) can be "commentable". But for purposes of demonstration, we'll use "sentinel" to refer to the arbitrary model that will have its own `comments` field.

More specifically, the instances of such sentinel – e.g. Sentinel with _id=1_, Sentinel with _id=2_, etc. – need to have their own related comments. This means having the ability to:

1. View a list of existing comments on sentinel _id=1_
2. Adding a comment (if logged in) on sentinel _id=2_
3. Deleting a comment (if made by an `author`)
4. Updating an added comment's `content` (if made by an `author`)
5. Toggling visibility of the comment to the public.

All instances of the `Sentinel` model therefore will need their own commenting actions.
