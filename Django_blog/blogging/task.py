from __future__ import absolute_import, unicode_literals
from .models import Person
from django.contrib.auth.forms import PasswordResetForm
from celery import shared_task
from django.contrib.auth.models import User
import string
from django.shortcuts import render
from urllib import request
# from django.contrib.auth.models import User
from user.models import User
from django.utils.crypto import get_random_string

from celery import shared_task

from importlib import import_module
from django.conf import settings
# from django.contrib.sessions.models import Session
# from django.contrib.sessions.backends.db import SessionStore
from django.contrib import auth
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import base64
from django.utils.html import strip_tags
import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task
from django.db.models import Q
from importlib import import_module
from django.conf import settings
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import auth
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
import base64
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

User = get_user_model()



@shared_task
def create_random_user_accounts(mail):
    email_template_name = "./password_reset_email.html"
    associated_users = User.objects.filter(Q(email=mail))
    print(associated_users)
    if associated_users.exists():
        for user in associated_users:
            print("user", user.pk)
            c = {
                "email": mail,
                'domain': '127.0.0.1:8000',
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            plain_message = strip_tags(email)
            print(urlsafe_base64_encode(force_bytes(user.pk)))
            send_mail("subject", plain_message, 'admin@example.com', [mail], fail_silently=False, html_message=email)
        return email


    
# @shared_task
# def send_mail(subject_template_name, email_template_name, context,
#               from_email, to_email, html_email_template_name):
#     context['user'] = User.objects.get(pk=context['user'])

#     PasswordResetForm.send_mail(
#         None,
#         subject_template_name,
#         email_template_name,
#         context,
#         from_email,
#         to_email,
#         html_email_template_name
#     )