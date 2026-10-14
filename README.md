# Django Blog

A multi-user blogging platform with both server-rendered pages and a REST API. Users write, edit and tag posts, like or dislike other people's posts, and can turn on two-factor authentication.

Built in 2022. Django 2.2, Django REST Framework, Celery, PostgreSQL or SQLite.

## Features

- **Posts.** Create, edit and delete posts with a category, tags (django-taggit), an optional image or video, and a view counter. Paginated listing and keyword search.
- **Reactions.** Like and dislike on any post.
- **Profiles.** Per-user profile page with a profile picture upload.
- **Auth, several ways.** Email and password, JWT auth for the REST API, social login through GitHub, Twitter and Facebook (python-social-auth), password change, and email-based password reset.
- **Two-factor auth.** TOTP one-time codes through a bundled `django_mfa` app, with enable, disable and verify-at-login screens.
- **Background email.** Password reset and notification emails go out through Celery so the request returns immediately.
- **Custom permissions.** Only a post's author can edit or delete it, enforced in DRF permission classes.

## Project layout

```
Django_blog/
  Django_blog/   settings, URLs, WSGI/ASGI
  blogging/      posts, likes, search, REST API, Celery tasks
  user/          custom user model
  uprofile/      profile pages and pictures
  django_mfa/    TOTP two-factor auth
```

## REST endpoints

| Method | Path | Does |
| --- | --- | --- |
| GET | `/list/` | Paginated posts |
| GET | `/detail/<slug>` | One post |
| GET | `/pro/<uuid>` | A user's profile |
| POST | `/pro_pic/<uuid>` | Update profile picture |
| GET | `/search/` | Search posts |

## Run it locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirments.txt
cd Django_blog
# set SECRET_KEY, EMAIL_HOST_PASSWORD and the social auth keys as environment variables
python manage.py migrate
python manage.py runserver
```

Celery uses RabbitMQ (`amqp://localhost`) as its broker for emails:

```bash
celery -A blogging worker -l info
```
