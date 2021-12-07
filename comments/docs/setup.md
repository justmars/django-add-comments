# Setup

## Load virtual env

```zsh
.venv> poetry add django-add-comments # pip3 install django-add-comments
```

Will include dependencies from [pyproject.toml](../../pyproject.toml):

```toml
python = "^3.8"
Django = "^4.0"
django-extensions = "^3.1.5"
django-crispy-forms = "^1.13.0"
```

## Add app to project settings

```python
# in project_folder/settings.py
INSTALLED_APPS = [
    ...,
    'crispy_forms',  # add crispy_forms at least > v1.13, if not yet added
    'comments' # this is the new django-comments folder
]
```

## Add basic routes to urlpatterns

```python
# in project_folder/urls.py
from django.urls import path, include # new
urlpatterns = [
    ...,
    path('comments/', include('comments.urls')) # routes for update, delete, view, toggle comment
]
```

## Add Comment model to database

```zsh
.venv> python manage.py migrate
```
