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
>>> obj = Sentinel.objects.create(title="A sample title") # instance is made, e.g. id=1, id=2, etc.
>>> obj.add_comment_url # url to add a comment to `A sample title`
```

## Quickstart

1. [Install app](./comments/docs/setup.md)
2. [Configure backend](./comments/docs/backend.md)
3. [Understand frontend](./comments/docs/frontend.md)
