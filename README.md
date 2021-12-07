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

## Quickstart

1. [Install](./comments/docs/setup.md) django-add-comments app
2. [Copy / paste snippets](./comments/docs/add_comments.md) to enable features

[^1]: [No page refresh](./comments/docs/frontend.md)
