# Newcastle Games Convention: Setup Guide

This guide explains how to recreate the basic Django site, connect its homepage and stylesheet, apply migrations, and run it locally.

## Requirements

- Windows and PowerShell
- Python. This project was checked with Python 3.14.7 and Django 6.1.1.
- The `py` Python launcher, or use `python` in its place if that is the command available on your machine.

## Create a Fresh Project

Open PowerShell in the parent folder where you want the project. These commands create a virtual environment, install Django, and create the project and app:

```powershell
mkdir NGC
cd NGC
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install Django==6.1.1
python -m django startproject NGC .
python manage.py startapp pages
```

The final `.` in `startproject NGC .` is important: it creates `manage.py` in the current folder. If PowerShell blocks virtual-environment activation, run the Python commands directly with `\.venv\Scripts\python.exe` instead, for example `\.venv\Scripts\python.exe -m pip install Django==6.1.1`.

For this project, the folder containing `manage.py` is `Newcastle Games Convention\NGC`. Run all `manage.py` commands from that folder.

## Connect the App

In `NGC/settings.py`, add the app configuration to `INSTALLED_APPS`:

```python
'pages.apps.PagesConfig',
```

Keep `django.contrib.staticfiles` in `INSTALLED_APPS`, `APP_DIRS` set to `True` in `TEMPLATES`, and `STATIC_URL = 'static/'` in the settings.

Create `pages/urls.py`:

```python
from django.urls import path

from . import views

urlpatterns = [
 path('', views.home, name='home'),
]
```

In `NGC/urls.py`, import `include` and include the app's URL configuration at the site root:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
path('admin/', admin.site.urls),
 path('', include('pages.urls')),
]
```

The filename and include must both say `urls.py` / `pages.urls` (plural).

## Render the Homepage

Set `pages/views.py` to render the template:

```python
from django.shortcuts import render


def home(request):
return render(request, 'pages/index.html')
```

Create the template at `pages/templates/pages/index.html`:

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Newcastle Games Convention">
<title>Newcastle Games Convention</title>
<link rel="stylesheet" href="{% static 'pages/style.css' %}">
</head>
<body>
<header>
<h1>Newcastle Games Convention</h1>
</header>
<main>
<p>Welcome to Newcastle Games Convention.</p>
</main>
</body>
</html>
```

`{% load static %}` enables Django's static-file tag. The `href` asks Django to generate the stylesheet URL; do not link to a Windows filesystem path.

## Add the Stylesheet

Create the CSS file at `pages/static/pages/style.css`. The first `pages` is the app's static folder; the second `pages` namespaces this app's files and is part of the URL used in the template.

```css
:root {
color-scheme: light;
--ink: #242820;
--paper: #f4f3ed;
--accent: #b8402e;
--header: #e4e9df;
}

* {
box-sizing: border-box;
}

body {
margin: 0;
background: var(--paper);
color: var(--ink);
font-family: Georgia, "Times New Roman", serif;
line-height: 1.6;
}

header {
padding: 2rem max(1.5rem, calc((100vw - 68rem) / 2));
background: var(--header);
border-bottom: 4px solid var(--accent);
}

h1 {
margin: 0;
font-size: 2.5rem;
line-height: 1.15;
}

main {
max-width: 71rem;
margin: 0 auto;
padding: 2.5rem 1.5rem;
}

main p {
font-family: "Trebuchet MS", sans-serif;
font-size: 1.125rem;
}
```

## Check, Migrate, and Run

From the folder containing `manage.py`:

```powershell
python manage.py check
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser. Leave the terminal running while you use the site; press `Ctrl+C` in that terminal to stop the server. Django's development server automatically reloads Python changes. Refresh the browser after editing CSS; use `Ctrl+F5` if the old styling remains cached.

Useful checks:

```powershell
python manage.py showmigrations
python manage.py findstatic pages/style.css
```

`migrate` applies migrations that already exist, including Django's built-in database tables. After changing a model in `pages/models.py`, create a migration and then apply it:

```powershell
python manage.py makemigrations
python manage.py migrate
```

## Common Problems

- **`py` is not recognized:** Install the Python Install Manager or run the same commands with `python`. If Python is installed but `py` is not found, check that `%USERPROFILE%\AppData\Local\Microsoft\WindowsApps` is on your user PATH, then open a new terminal.
- **`No module named 'pages.url'`:** The module is named `pages.urls` (plural); make the include match `pages/urls.py`.
- **`manage.py` cannot be found:** Change directory to the project folder that contains `manage.py` before running commands.
- **Template not found:** Check that the app is registered in `INSTALLED_APPS` and the file is at `pages/templates/pages/index.html`.
- **Stylesheet is missing:** Check that the file is at `pages/static/pages/style.css`, that the template has `{% load static %}`, and that the link uses `{% static 'pages/style.css' %}`. `python manage.py findstatic pages/style.css` should print the file's location.
- **`runserver` exits:** Read the error printed above the exit status. Fix that error, then run `python manage.py check` before trying again.

The Django development server is for local development only. Before putting the site on the public internet, configure production settings, keep the secret key out of source control, set `DEBUG = False`, and use a production web server.
