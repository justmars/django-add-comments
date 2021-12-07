# Setup

## Install within your virtual environment

```zsh
.venv> pip3 install django-add-comments # poetry add django-add-comments
```

## Add aapp to project settings

```python
# in project_folder/settings.py
INSTALLED_APPS = [
    ...,
    'crispy_forms',  # add crispy_forms at least > v1.13, if not yet added
    'comments' # this is the new django-comments folder
]
```

## Add new routes to project urlspatterns

```python
# in project_folder/urls.py
from django.urls import path, include # new
urlpatterns = [
    ...,
    path('comments/', include('comments.urls')) # new
]
```

## Add Comment model to database

```zsh
.venv> python manage.py migrate
```
