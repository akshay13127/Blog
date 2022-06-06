from django.core.exceptions import PermissionDenied
from user.models import User
from functools import wraps
from django.http import HttpResponseRedirect
from rest_framework_jwt.settings import api_settings
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER
from django.http import HttpResponse, JsonResponse
from social_django.models import UserSocialAuth

import json
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def user_is_authenticated(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        a = request.headers.get('Authorization')
        # ab = args[0].headers.get('Authorization')
        # a = request.headers['Authorization']
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@',a, 'dgfkhgdafkjhgdashfghdasghf' ,ab)
        token_obj = a
        d_token = JWT_DECODE_HANDLER(token_obj)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@',d_token)
        kwargs['u_id'] = d_token['user_id']
        if User.objects.filter(id = d_token['user_id']).exists():
            return func(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap

import uuid
from django.contrib.auth.models import update_last_login

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


def soical_auth(func):
    @wraps(func)
    def wrap(request, *args, **kwargs):
        id3 = request.user
        user = UserSocialAuth.get_social_auth('google-oauth2',id3)
        # uid = json.dumps(user.user_id, cls=UUIDEncoder)
        # uidd = uid.replace('"', '')
        # id1 = request.session._session_cache['_auth_user_id']
        credientials = None
        try:
            credientials = user.extra_data['access_token']
            user1 = User.objects.filter(id=user.user_id).first()
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@',user1.pk)

        except:
            pass
        if credientials == None:
            print("sdjfhlasdjhfjadhjfhjadhfjkadhfjahdsjkfhjdksahfjdashjhdsjkhfjkasdhjk")
            return func(request, *args, **kwargs)
        else:
            if not request.session.has_key('person_id'):
                request.session['person_id'] = str(user1.id)
                request.session['person_name'] = user.uid
                try:
                    payload = JWT_PAYLOAD_HANDLER(user1)
                    jwt_token = JWT_ENCODE_HANDLER(payload)
                    update_last_login(None, user1)
                    print(jwt_token,'#$$$$$#$####################$#$')
                    kwargs['token'] = jwt_token
                    request.session['token'] = jwt_token
                except User.DoesNotExist:
                    raise serializers.ValidationError('User with given email and password does not exists')
                

        # if User.objects.filter(id = d_token['user_id']).exists():
        #     return func(request, *args, **kwargs)
        # else:
        #     raise PermissionDenied
        return func(request, *args, **kwargs)

    return wrap


