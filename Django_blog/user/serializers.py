
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 11:14:00 2019
@author: sambhav
"""
from rest_framework import serializers
from blogging.models import Person
from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ('fname', 'lname', 'contact', 'city', 'state')


class UserRegistrationSerializer(serializers.ModelSerializer):

    person = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'person')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        profile_data = validated_data.pop('person')
        user = User.objects.create_user(**validated_data)
        Person.objects.create(
            user=user,
            fname=profile_data['fname'],
            lname=profile_data['lname'],
            contact=profile_data['contact'],
            city=profile_data['city'],
            state=profile_data['state']
        )
        return user


from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from user.models import User
from rest_framework.response import Response

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    id = serializers.CharField(max_length=255,read_only=True)
    
    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('A user with this email and password is not found.')
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with given email and password does not exists')
        return {
            'email':user.email,
            'token': jwt_token,
            'id':user.id
        }