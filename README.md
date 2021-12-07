# django-add-comments

Adds a `comments` field to a Django model via a `AbstractCommentable` mixin. As an effect, model instances – e.g. `Sentinel` with _id=1_, `Sentinel` with _id=2_, etc. – will have basic create functionality `Comment`s.

```python
# app/models.py
from comment.models import AbstractCommentable # import mixin
class Sentinel(AbstractCommentable): # add to class declaration
    """Any `app`, e.g. `essay`, `article`... can be 'commentable'."""
    title = models.CharField(max_length=50)
```

## Features

Includes ability to:

1. View a list of existing comments on a given 'sentinel' _id=1_
2. Adding a comment on given 'sentinel' _id=2_[^1]
3. Deleting a comment[^2]
4. Updating an added comment's `content` field and `is_public` checkbox.[^2]

[^1]: Requires authentication
[^2]: Requires author authorization (simple permission checking)

## Quickstart

1. [Install](./comments/docs/setup.md) django-add-comments app
2. [Configure](./comments/docs/add_comments.md) target model's properties, urls, template
3. Once setup, explore the htmx-driven [frontend](./comments/docs/frontend.md).
