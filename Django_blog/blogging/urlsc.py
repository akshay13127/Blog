from django.urls import path, include
from . import views
from .views import (
    BrandListCreateAPIView,  
    ReSet, 
    userlist, 
    SendView, 
    Personview, 
    Changepassword, 
    UpdatePost, 
    PostListAPIView, 
    UserLoginAPIView, 
    PostDetailAPIView, 
    PostCreate, 
    UserCreate, 
    ProfileView, 
    PostDeleteAPIView, 
    ProfilePictureUpdateView
    )
from django.conf.urls import url

app_name = 'blogg'

urlpatterns = [

    path('l/',BrandListCreateAPIView.as_view() , name= "l"),
    path('user_list/',Personview.as_view() ,name= "user_list"),
    # path('SendMail/',views.SendMail , name= "SendMail"),
    path('SendMail/',SendView.as_view() , name= "SendMail"),
    path('View/',Personview.as_view() , name= "View"),
    # path('ResetPassword/<uidb64>/<token>/',views.ResetPassword , name= "ResetPassword"),
    path('ResetPassword/<uidb64>/<token>/', ReSet.as_view() , name= "ResetPassword"),
    # path('signup/',views.signup , name= "signup"),
    # path('login/',views.login , name= "login"),
    path('logout/<uuid:pk>', views.logout, name='logout'),
    # path('profile/', views.profile, name='profile'),
    path('delete_blog/', views.delete_blog, name='delete_blog'),
    path('search/',views.search,name='search'),
    # path('autosuggest/', views.autosuggest, name= 'autosuggest'),
    # path('editblog/', views.editblog, name='editblog'),
    # path('editprofile/', views.editprofile, name='editprofile'),
    # path('Image', views.Image, name='Image'),
    # path('blogss/', views.blogss, name='blogss'),
    # path('allblogs/', views.allblogs, name='allblogs'),
    # path('like', views.Like, name='like'),
    
    path('list/', PostListAPIView.as_view(), name='list'),
    path('detail/<slug>', PostDetailAPIView.as_view(), name='detail'),
    path('pro/<uuid:pk>', ProfileView.as_view(), name='pro'),
    path('pro_pic/<uuid:pk>', ProfilePictureUpdateView.as_view()),
    # path('delete_blog/', PostDeleteAPIView.as_view(),name='delete_blog'),
    # path('pro/ed/<int:pk>', ProfileView.as_view(), name='ed'),
    # url(r"^(?P<slug>[\w-]+)/edit/$", PostUpdateAPIView.as_view(), name='edit'),
    url('create/', PostCreate.as_view(), name='create'),
    url('uv/', UserCreate.as_view(), name='uv'),
    path('log/', UserLoginAPIView.as_view(), name='log'),
    url('edit/', UpdatePost.as_view(), name='edit'),
    path('change_password/', Changepassword.as_view(), name='change_password'),
    path('hello/', views.HelloView.as_view(), name='hello'),



    # path('blog_post/', views.blog_post, name='post'),
    path('', views.index, name='index'),
    # path('blog_detail/<slug>', views.blog_detail, name='blog_detail'),

]
