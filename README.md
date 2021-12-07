# django-add-comments

Add `comments` field to a Django model:

```python
# app/models.py
from comment.models import AbstractCommentable # import mixin
class Sentinel(AbstractCommentable): # add to class declaration
    """Any `app`, e.g. `essay`, `article`... can be 'commentable'."""
    title = models.CharField(max_length=50)
```

## Quickstart

1. [Install](./comments/docs/setup.md) django-add-comments app
2. [Configure](./comments/docs/add_comments.md) target model's properties, urls, template

## Features

Built-in functions:

1. View list of existing comments on a given 'sentinel'[^1] via a template tag
2. Display a comment form on given 'sentinel'[^2] allowing reactive submissions [without page refresh](./comments/docs/frontend.md)
3. Delete a comment[^3]
4. Update an added comment's `content` field and `is_public` checkbox[^3]

[^1]: All users, whether or not authenticated
[^2]: Only authenticated users authorized
[^3]: Only authenticated authors authorized (simple permission checking)
