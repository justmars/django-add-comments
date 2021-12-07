# django-add-comments

Adds a `comments` field to a Django model via a `AbstractCommentable` mixin.

```python
# app/models.py
from comment.models import AbstractCommentable # import mixin
class Sentinel(AbstractCommentable): # add to class declaration
    """Any `app`, e.g. `essay`, `article`... can be 'commentable'."""
    title = models.CharField(max_length=50)
```

## Features

Each comment will have create-read-update-delete (CRUD) functionality. Specifically:

1. View a list of existing comments on a given 'sentinel' [^1]
2. Adding a comment on given 'sentinel' [^2]
3. Deleting a comment[^3]
4. Updating an added comment's `content` field and `is_public` checkbox.[^3]

[^1]: All users, whether or not authenticated
[^2]: Only authenticated users authorized
[^3]: Only authenticated authors authorized (simple permission checking)

## Quickstart

1. [Install](./comments/docs/setup.md) django-add-comments app
2. [Configure](./comments/docs/add_comments.md) target model's properties, urls, template
3. Once setup, explore the htmx-driven [frontend](./comments/docs/frontend.md).
