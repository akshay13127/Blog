from django.shortcuts import render

# Create your views here.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  20 14:04:16 2021
@author: akshay
"""
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
# from blogging.utils import create_response_formatt
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user.serializers import UserRegistrationSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from .models import User
from rest_framework import renderers

class UserRegistrationView(CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'signup.html'
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    
    def get(self, request):
        profile = User.objects.all()
        serializer = UserRegistrationSerializer(profile)
        return Response({'serializer': serializer})

    def post(self, request):
        url = request.META.get('HTTP_REFERER')
        print(request.data)
        print(request.POST,'dsafffffffffffffffffffffffffffffffffffffffffffffffffffffhhhhhh')
        if User.objects.filter(email=request.data['email']).exists():
            msg = messages.error(request, "Email already exists!!!!!!!!!!!!!")
            return JsonResponse(create_response_format(msg=msg ,success=False, status=400))
        else:
            serializer = self.serializer_class(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            # print(serializer)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                'message': 'User registered  successfully',
                }
            
            return JsonResponse(create_response_format(msg="You're Register Successfully...",success=True,redirect="/api/signin/", is_valid=True, status=status.HTTP_200_OK))


from django.shortcuts import render, redirect, HttpResponseRedirect
import requests
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user.serializers import UserLoginSerializer
from rest_framework.authtoken.models import Token
import uuid
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from rest_framework.parsers import JSONParser
from django_mfa.models import is_u2f_enabled
from .custom_response import create_response_format


class UserLoginView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login.html'
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    # parser_classes = [JSONParser]
    # queryset = User.objects.all()


    def get(self, request):
        profile = User.objects.all()
        serializer = UserLoginSerializer(profile)
        return Response({'serializer': serializer})

    def post(self, request):
        url = request.META.get('HTTP_REFERER')
        obj = authenticate(email=request.data['email'],password= request.data['password'])
        print(obj)
        if obj != None:
            serializer = self.serializer_class(data=request.data)
            
            if serializer.is_valid():
                request.session['person_id'] = serializer.data['id']
                request.session['person_name'] = serializer.data['email']
                user=User.objects.get(email=serializer.data['email'])
                if is_u2f_enabled(user):
                    request.session['u2f_pre_verify_user_pk'] = user.pk
                    request.session['u2f_pre_verify_user_backend'] = user.backend
                user.backend='django.contrib.auth.backends.ModelBackend'
                login(request, user)
                
                messages.success(request, "You are sucessfully login..")
                print(serializer.data['token'],"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                #create_response_formatt(msg="Successfully Login...",success=True,redirect="/settings/security/", token=serializer.data['token'],is_valid=True, status=200)
                # html_form = render_to_string('login.html', response)
                return JsonResponse(create_response_format(msg="Successfully Login...",success=True,redirect="/settings/security/", token=serializer.data['token'],is_valid=True, status=status.HTTP_200_OK))
                # return redirect('/settings/security')
                # return redirect('/')
        else:
            msg = messages.error(request, "Email or Password is incorrect!!!!")
            return JsonResponse(create_response_format(msg=msg ,success=False, status=400))

