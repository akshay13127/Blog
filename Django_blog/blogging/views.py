from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import Person, Blog, Like, Dislike
# This requires the user to be logged in.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_protect, csrf_exempt
# Create your views here.
# from django.views.decorators import api_view
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import datetime
from .custom_decoreter import user_is_authenticated, soical_auth
from django.db.models import Q
from django.contrib import auth
from django.views import View 

from rest_framework import viewsets
from .serializers import (
    PersonSerializer, 
    changep, 
    PostListSerializer, 
    UserLoginSerializer, 
    PostDetailSerializer, 
    PersonListSerializer, 
    CreatePostSerializer, 
    ProfileDetailSerializer, 
    ProfileSerializer, 
    PostCreateUpdateSerializer, 
    PersonCreateSerializer
    )
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, HTMLFormRenderer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    GenericAPIView,
    ListCreateAPIView
    )
from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )
from .permissions import IsOwnerOrReadOnly

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

from .pagination import PageNumberPagination, CustomPagination
from user.custom_response import create_response_format
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.views.generic import ListView, TemplateView
from .forms import GenerateRandomUserForm
from .task import create_random_user_accounts
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from social_django.models import UserSocialAuth
# from oauth2client.contrib.django_util.storage import DjangoORMStorage
# from oauth2client.contrib.django_util.models import CredentialsField
import requests
from google.oauth2 import id_token
from google.auth.transport import requests


@soical_auth
@login_required
def index(request, *args, **kwargs):
    blogs = Blog.objects.all()
    # print(request.data)
    # idinfo = id_token.verify_oauth2_token(token, requests.Request(), SOCIAL_AUTH_GOOGLE_OAUTH2_KEY)
    print(request.META.get('HTTP_X_APIKEY', None))
    from rest_framework.authentication import BaseAuthentication, get_authorization_header
    from rest_framework import exceptions, HTTP_HEADER_ENCODING
    auth_header = get_authorization_header(request).decode(HTTP_HEADER_ENCODING)
    # storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential') 
    # credential = storage.get() 
    id1 = request.session._session_cache['_auth_user_id']
    id2 = Person.objects.filter(user_id=id1).first()
    id3 = request.user
    user = UserSocialAuth.get_social_auth('google-oauth2',id3)
    # response = requests.get(
    # 'http://127.0.0.1:8000/oauth/complete/google-oauth2',
    # params={'access_token': user.extra_data['access_token']}
    # )
    # # friends = response.json()
    # print(response)
    if user:
        print(user.extra_data)
    if not request.session.has_key('person_id'):
        request.session['person_id'] = id1
        request.session['person_name'] = user.uid

    # print(User.objects.filter(social_auth=request.user.id).first())
    try:
        id1 = request.session._session_cache['_auth_user_id']
        id2 = Person.objects.filter(user_id=id1).first()
        jwt_token = kwargs['token']
        # return JsonResponse({'token':jwt_token})
        return render(request, 'index.html', {'blogs': blogs, 'id2':id2})
    except:
        pass
    return render(request, 'index.html',{'id1':id1})


def search(request):
    kw = request.GET.get('keyword')
    results = Blog.objects.filter(Q(title__icontains=kw) | Q(
        slug__icontains=kw) | Q(Content__icontains=kw))
    if kw != "":
        if results:
            return render(request, 'search.html', {'results': results})
        else:
            messages.error(request, kw + " Not Found !!!!!!")
            return render(request, 'search.html')

    else:
        messages.error(request, kw + " Not Found !!!!!!")
        return render(request, 'search.html')


class SendView(View):
    
    def post(self, request):
        if request.method == 'POST':
            mail = request.POST.get('email')
            cel = create_random_user_accounts.delay(mail)
            print(cel)
            return redirect('../SendMail')
        # return render(request, 'SendMail.html')

    def get(self, request):
        if request.session.has_key('person_id'):
            return redirect('/')
        else:
            return render(request, 'SendMail.html')

class userlist(ListView):
    template_name = './user_list.html/'
    model = Person

import uuid

# @csrf_exempt
def logout(request, pk):
    auth.logout(request)
    print(auth.logout(request))
    # Session.objects.filter(session_key=request.session.session_key).delete()
    return redirect(f'../api/signin')


def delete_blog(request):
    url = request.META.get('HTTP_REFERER')
    if request.session.has_key('person_id'):
        u_id = request.session['person_id']
        if request.method == 'POST':
            b_id = request.POST.get('blog_id')
            if Blog.objects.filter(id=b_id, uname_id=u_id):
                de = Blog.objects.get(id=b_id)
                de.delete()
                messages.success(request, "Post deleted Successfuly.......")
            else:
                messages.error(request, "you are not author..")
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)



      

class Personview(APIView):
    # renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user_list.html'
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

     
    def get(self, request):
        data01 = Person.objects.all().order_by('-fname')
        serializer = PersonSerializer(data01, many=True)
        data = serializer.data
        return Response({"data": data})

from user.models import User
from rest_framework_jwt.settings import api_settings
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER
from .permissions import TokenRequired

from django.utils.decorators import method_decorator
from rest_framework import pagination


class BrandListCreateAPIView(ListAPIView):

    serializer_class = PostListSerializer
    pagination_class = CustomPagination
    queryset = Blog.objects.all()

class PostListAPIView(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = PostListSerializer
    queryset = Blog.objects.all()
    lookup_field = 'slug'
    pagination_class = CustomPagination
    template_name = 'allblog.html'

    # @method_decorator(user_is_authenticated)
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = PostListSerializer(page, context={'request': request}, many=True)
        print('@@@@@@@@@@@@@@@###########',self.get_paginated_response(serializer.data))
        return self.get_paginated_response(serializer.data)



class PostDetailAPIView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Blog.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    template_name = 'detail.html'


class PostCreate(APIView):
    # queryset = Blog.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    # serializer_class = CreatePostSerializer
    template_name="post.html"

    # @method_decorator(user_is_authenticated)
    def get(self, request):
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')     
        blog = Blog.objects.all()
        serializer = CreatePostSerializer(blog,many=True)
        return Response({'data':serializer.data})   

    @method_decorator(user_is_authenticated)
    def post(self, request, *args, **kwargs):
        url = request.META.get('HTTP_REFERER')
        u_obj = kwargs['u_id']
        if u_obj:
            context={}
            print(request.is_ajax())
            if request.is_ajax():
                message = "This is ajax"

            context['title']=request.POST.get('title')
            context['Content']=request.POST.get('Content')
            context['uname']=request.POST.get('uname')
            context['category'] = "Coding"
            context['author'] = request.session['person_name']        
            context['slug']=request.POST.get('title')
            if request.FILES.get('photos') is not None:
                context['photos'] = request.FILES.get('photos')
            

            serializer = CreatePostSerializer(data=context, partial=True)
            print(context)  
            if serializer.is_valid():
                serializer.save()
                print('djhajkhakj')
                messages.success(request, "Blog is successfully post....")
                # return HttpResponseRedirect(url)
                return JsonResponse(create_response_format( data=serializer.data, msg="Blog Post Successfully...", success=True,is_valid=True, status=status.HTTP_200_OK))
            else:
                message = "Not ajax"
            return HttpResponse(message)
        else:
            messages.error(request, "You're not login!!!")
            # return HttpResponseRedirect(url)
            return JsonResponse(create_response_format(msg=msg ,success=False, status=400))


import jwt

class UserCreate(CreateAPIView):
    # queryset = Blog.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = PersonCreateSerializer
    template_name="signup.html"
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        user = Person.objects.all()
        serializer = UserLoginSerializer(user,many=True)
        return Response({'data':serializer.data})

    def post(self, request, format=None):
        context={}
        context['fname']=request.POST.get('firstname')
        context['lname']=request.POST.get('lastname')
        context['email']=request.POST.get('email')
        context['contact'] = request.POST.get('contact')
        context['password'] = request.POST.get('password')
        password12 = request.POST['repassword']
        user_qs = Person.objects.filter(email=request.POST.get('email'))
        if user_qs.exists():
            messages.error(request, "This email is already exists!!!!")
            return redirect("/uv/")
        else:
            if password12 == context['password']:

                # context['photos'] = request.FILES.get('image') 
                serializer = PersonCreateSerializer(data=context, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    print('djhajkhakj')
                    return redirect('/log/')  
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                messages.error(request, "Password Didn't Match")
                return redirect("/uv/")


class UserLoginAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name="login.html"
    # permission_classes = (IsAuthenticated,)
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def get(self, request, format=None):
        user = Person.objects.all()
        serializer = UserLoginSerializer(user,many=True)
        return Response({'data':serializer.data})

    def post(self, request, *args, **kwargs):
        url = request.META.get('HTTP_REFERER')
        data = request.data
        person_obj = Person.objects.filter(email = request.POST['email']).first()
        pid = person_obj.id
        context = {}
        context["password"] = request.data["password"]
        context["email"] = request.data["email"]
        # token, created = Token.objects.get_or_create(user=pid)
        # data['token'] = token
        print(request.data)
        obj = Person.objects.filter(email=request.data['email'],password= request.data['password'])
        if obj.exists():
            user = obj.first()
            token1=jwt.encode({'username': user.fname,"id":user.id}, "secret", algorithm="HS256")
            # request.POST['token'] = token
            print(token1)
            context["token"] = token1
            print(context["token"])
            # request.data[{'token':token}]
            print(request.data['token'])
            serializer = UserLoginSerializer(data=context)
            if serializer.is_valid(raise_exception=True):
                new_data = serializer.data
                request.session['person_id'] = user.id
                request.session['pname'] = user.fname
                messages.success(request, "You are sucessfully login..")
                return redirect('/')
        else:
            return HttpResponseRedirect(url)


class ProfilePictureUpdateView(APIView):
    serializer_class = PersonSerializer
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Person.objects.all()
    template_name="profile.html"
    
    # @method_decorator(user_is_authenticated)
    def post(self, request, pk, *args, **kwargs):
        print(request.POST,"################")
        # u_id = kwargs['u_id']
        if request.session['person_id']:
            url = request.META.get('HTTP_REFERER')
            print(request.data['photo'])
            picture = Person.objects.filter(user_id=pk).first()
            serializer = PersonSerializer(picture, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                
                return JsonResponse(create_response_format(msg="Successfully Updated...",success=True ,is_valid=True, status=status.HTTP_200_OK))

            print("dsafffffffffffffffffffffffffffffffffffffffffffffffffffff")
            return JsonResponse(create_response_format(msg="something went wrong" ,success=False, status=400))
        else:
            return JsonResponse(create_response_format(msg="something went wrong" ,success=False, status=400))



class ProfileView(APIView):
    # permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile.html'
    lookup_url_kwarg = 'pk'
    queryset = Person.objects.all()


    def get(self, request, pk):
       
        # s = request.session['person_id']
        a1 = User.objects.filter(id = pk).first()
        b = a1.blog_set.all()
        print(a1)
        if Person.objects.filter(user_id=pk):
            profile = get_object_or_404(Person, user_id=pk)
            print(profile,'#########################')
            serializer = ProfileSerializer(profile)
            return Response({"person": serializer.data , 'profile': profile, 'b':b}) 
        else:
            profile1 = Person(user_id=pk).save()
            profile = get_object_or_404(Person, user_id=pk)
            print(profile,'@@@@@@@@@@@@@@@@@@@@@@')
            serializer = ProfileSerializer(profile)
        return Response({"person": serializer.data , 'profile': profile, 'b':b}) 
    
    def post(self, request, pk):
        url = request.META.get('HTTP_REFERER')
        print('dsffffafasdf',pk)
        profile = get_object_or_404(Person, user_id=pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'person': serializer.data, 'profile': profile})
        serializer.save()
        return HttpResponseRedirect(url) 



class UpdatePost(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (AllowAny,)
    template_name = 'blog_detail.html'
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    queryset = Blog.objects.all()
    
    def post(self, request):
        url = request.META.get('HTTP_REFERER')
        v = Blog.objects.filter(slug =request.POST.get("slug")).first()
        blogiz = PostDetailSerializer(v, data=request.data, partial=True)
        if blogiz.is_valid():
            blogiz.save()
            messages.success(request, "Blog Updated Successfully")
            return HttpResponseRedirect(url)
        messages.error(request, "Blog Could Not be updated.")
        return HttpResponseRedirect(url)




class PostDeleteAPIView(DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostListSerializer
    lookup_field = 'slug'



from user.serializers import UserRegistrationSerializer
from django.contrib.auth.hashers import make_password
class Changepassword(GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    permissions_classes = [AllowAny,]
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    lookup_field = ["password"]

    def post(self, request):
        url = request.META.get('HTTP_REFERER')
        print(request.data)
        if request.POST.get("password") == request.POST.get("confirm_pass"):
            all11 = User.objects.filter(id = request.session["person_id"]).first()
            st = UserRegistrationSerializer(all11 , data = {"password":request.data["password"]}, partial = True)
            if st.is_valid():
                st.save()
                instance = st.save()
                instance.set_password(instance.password)
                instance.save()
                messages.success(request , "your password has changed successfully..!")
                all11 = User.objects.filter(id = request.session["person_id"]).first()
                return HttpResponseRedirect(url)
            messages.error(request , "your password has changed successfully..!")
            all11 = User.objects.filter(id = request.session["person_id"]).first()
            return HttpResponseRedirect(url)
        else:
            messages.error(request , "your password did not matched please make it correct..!")
            all11 = User.objects.filter(id = request.session["person_id"]).first()
            return HttpResponseRedirect(url) 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class AjaxRedirect(object):
    def process_response(self, request, response):
        if request.is_ajax():
            if type(response) == HttpResponseRedirect:
                response.status_code = 278
        return response


class ReSet(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permissions_classes = [AllowAny,]
    template_name = 'password_reset_confirm.html'
    queryset = User.objects.all()
    serializer_class = changep
    # lookup_field = ["password"]

    def get(self, request, format=None, *args, **kwargs):
        user = User.objects.all()
        serializer = self.serializer_class(user,many=True)
        return Response({'data':serializer.data})

    def post(self, request, *args, **kwargs):
        id = (urlsafe_base64_decode(kwargs['uidb64']).decode())
        print('dlfjgjakglgaflgflhgadfhlgh',id)
        obj = User.objects.filter(id=id).first()
        token = default_token_generator.check_token(obj, kwargs['token'])
        url = request.META.get('HTTP_REFERER')
        print(request.POST.get("password"),request.POST.get("confirm_pass"))
        if request.POST.get("password") == request.POST.get("confirm_pass") and token:
            all11 = User.objects.filter(id = id).first()
            st = changep(all11 , data = {"password":request.data["password"]}, partial = True)
            if st.is_valid():
                instance = st.save()
                instance.set_password(instance.password)
                instance.save()
                messages.success(request , "your password has changed successfully..!")
                all11 = User.objects.filter(id = id).first()
                return HttpResponseRedirect(url)
            messages.error(request , "your password has changed successfully..!")
            all11 = User.objects.filter(id = id).first()
            return HttpResponseRedirect(url)

        else:
            messages.error(request , "your password did not matched please make it correct..!")
            all11 = User.objects.filter(id = id).first()
            return HttpResponseRedirect(url)