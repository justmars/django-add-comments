# django-add-comments

Add `comments` to a Django model via mixin:

```python
# app/models.py
from comment.models import AbstractCommentable # import mixin
class Sentinel(AbstractCommentable): # add to class declaration
    """Any `app`, e.g. `essay`, `article`... can be 'commentable'."""
    title = models.CharField(max_length=50)
```

## Quickstart

1. [Install](./comments/docs/setup.md) django-add-comments app
2. [Copy / paste snippets](./comments/docs/add_comments.md) to target model's properties, urls, template

## Commenting Features

| Action                                          | Description                                | Authorization                                   |
| ----------------------------------------------- | ------------------------------------------ | ----------------------------------------------- |
| View list comments on a sentinel                | Maybe filter public/private comments later | All users                                       |
| Get comment form when sentinel                  | Reactive add comment form via htmx [^1]    | Only authenticated users authorized to get/post |
| Delete / update comment (`content`, `is_public) | Simple permission checking                 | Only authenticated authors authorized           |

[^1]: [Without page refresh](./comments/docs/frontend.md)
