from django.shortcuts import render
from .models import Person, Blog, Like, Dislike
# This requires the user to be logged in.
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.csrf import csrf_protect, csrf_exempt
# Create your views here.
from django.contrib.auth.hashers import check_password
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import datetime
from django.db.models import Q
from django.contrib import auth
from django.views import View


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



def ResetPassword(request, *args, **kwargs):
    # id =(urlsafe_base64_decode(kwargs['uidb64']).decode())
    # obj=newUserDetails.objects.filter(userId =id).first()
    # token=default_token_generator.check_token(obj, kwargs['token'])
    
    #print('id',urlsafe_base64_decode(kwargs['uidb64']).decode())


    id = (urlsafe_base64_decode(kwargs['uidb64']).decode())
    print(id)
    obj = Person.objects.filter(id=id).first()
    token = default_token_generator.check_token(obj, kwargs['token'])
    if request.method == 'POST':
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        print(password, cpassword, token)
        if password == cpassword and token:
            Person.objects.filter(id=id).update(password=password)
            token = False
            messages.success(request, "Password Set Successfully")
            return redirect('/accounts/login')
        else:
            if token:
                messages.error(request, "Password and confirmpassword Dosen't match")
            else:
                messages.error(request, "Please regenerate the link this link is Invalid")
        return render(request, './password_reset_confirm.html',)
    return render(request, './password_reset_confirm.html',)




class GenerateRandomUserView(FormView):
    template_name = './generate.html/'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('../user_list')

class userlist(ListView):
    template_name = './user_list.html/'
    model = Person

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

# def SendMail(request):
#     if request.method == 'POST':
#         print('lkhdsfgjahjk;dlfnsjkla.')

#         mail = request.POST.get('email')
#         print(mail)
#         email_template_name = "./password_reset_email.html"
#         associated_users = Person.objects.filter(Q(email=mail))
#         print(associated_users)
#         if associated_users.exists():
#             for user in associated_users:
#                 print("user", user.pk)
#                 c = {
#                     "email": mail,
#                     'domain': '127.0.0.1:8000',
#                     'site_name': 'Website',
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "user": user,
#                     'token': default_token_generator.make_token(user),
#                     'protocol': 'http',
#                 }
#                 email = render_to_string(email_template_name, c)
#                 plain_message = strip_tags(email)
#                 send_mail("subject", plain_message, 'admin@example.com', [mail], fail_silently=False, html_message=email)
#         return render(request, "./SendMail.html",)
#     return render(request, "./SendMail.html")




 


def index(request):
    blogs = Blog.objects.all()
    print(blogs)
    try:
        id1 = request.session['person_id']
        id2 = Person.objects.filter(id=id1).first()
        return render(request, 'index.html', {'blogs': blogs, 'id2':id2})
    except:
        pass
    return render(request, 'index.html',)
   
# SignUp Function


def signup(request):
    # return render(request,'signup.html')
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        fname1 = request.POST['firstname']
        lname1 = request.POST['lastname']
        contact1 = request.POST['contact']
        email1 = request.POST['email']
        # state1 = request.POST['state']
        # city1 = request.POST['city']
        password1 = request.POST['password']
        password12 = request.POST['repassword']
        #now = datetime.datetime.now()
        if Person.objects.filter(email=email1).exists():
            messages.error(request, "This email is already exits!!!!")
            return HttpResponseRedirect(url)
        else:
            if password1 == password12:
                x = Person(fname=fname1, lname=lname1,
                           contact=contact1, email=email1, password=password1)
                x.save()

                messages.success(request, "You are Registered Successfully")
                return render(request, 'signup.html')
            else:
                return HttpResponse("your password did not match..!")

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email1 = request.POST['email']
        password1 = request.POST['password']
        a = Person.objects.filter(email=email1).first()
        votes_table = Person.objects.filter(
            email=email1, password=password1).exists()
        if votes_table:
            request.session['person_id'] = a.id
            request.session['pname'] = a.fname
            messages.success(request, "You are sucessfully login..")
            return redirect('blog:index')
        else:
            all1 = {"votes_table": '0'}
            request.session.clear()
            context = {"all1": all1}
            messages.error(request, "Invaild email or password !!!")
            return render(request, 'login.html')

    return render(request, 'login.html')


# def logout(request):
#     Session.objects.all().delete()
#     return redirect('blog:login')
@csrf_exempt
def logout(request):
    auth.logout(request)
    # Session.objects.filter(session_key=request.session.session_key).delete()
    return redirect(f'/accounts/login')

def allblogs(request):
    blog = Blog.objects.all()
    paginator = Paginator(blog, 3)
    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        queryset1 = paginator.page(1)
    except EmptyPage:
        queryset1 = paginator.page(paginator.num_pages)
    return render(request, 'allblog.html', {'page_obj': queryset1})

def blogss(request):
    blog = Blog.objects.all()
    paginator = Paginator(blog, 3)
    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        queryset1 = paginator.page(1)
    except EmptyPage:
        queryset1 = paginator.page(paginator.num_pages)
    return render(request, 'allblogs.html', {'page_obj': queryset1})


def profile(request): 
    if request.session.has_key('person_id'):
        id_u = request.session['person_id']
        per_obj = Person.objects.filter(id=id_u).first()
        id_obj = per_obj.id
        blog = Blog.objects.filter(username_id=id_obj)
        paginator = Paginator(blog, 2)
        page = request.GET.get('page')
        try:
            queryset1 = paginator.page(page)
        except PageNotAnInteger:
            queryset1 = paginator.page(1)
        except EmptyPage:
            queryset1 = paginator.page(paginator.num_pages)
    # print(blog)
    return render(request, 'profile.html', {'blog': blog, 'person': per_obj, 'page_obj': queryset1})


def blog_detail(request, slug):
    b = Blog.objects.filter(slug=slug).first()
    print(b)
    return render(request, 'blog_detail.html', {'b': b})

# @login_required(login_url='/login/')


def blog_post(request):
    if request.method == 'POST':
        id = request.session['person_id']
        all11 = Person.objects.filter(id=id).first()
        title1 = request.POST['name']
        Content1 = request.POST['allContent']
        # Tag = request.POST['tages']
        tages1 = request.POST.get("tages")
        image11 = request.FILES.get("image")
        # video1  = request.FILES.get("videofile")
        print("=============================================>", tages1)
        now = datetime.datetime.now()
        if Blog.objects.filter(title=title1).exists():
            if title1.isdigit():
                messages.error(
                    request, "This title only contains number please specify proper title..!")
                return render(request, 'post.html', {"title1": title1, "Content1": Content1})
            else:
                messages.error(
                    request, "This title already exists please try to choose another title for your blog..!")
                return render(request, 'post.html', {"title1": title1, "Content1": Content1})
        elif title1.isdigit():
            messages.error(
                request, "This title only contains number please specify proper title..!")
            return render(request, 'post.html', {"title1": title1, "Content1": Content1})
        else:
            if image11:
                messages.success(
                    request, "Your blog has posted successfully..!")
                st = Blog(title=title1, author=all11.fname,
                          username_id=all11.id, slug=title1, Content=Content1)
                st.save()
                sk = Blog.objects.filter(
                    username_id=all11.id, title=title1).first()
                sk.photos = image11
                sk.save()
                # if video1:
                #     messages.success(request ,"Your blog has posted successfully..!")
                #     st = Blog(title=title1, author=all11.fname, username_id = all11.id ,slug = title1, Content=Content1,video = video1)
                #     st.save()
                #     sk = Blog.objects.filter(username_id = all11.id, title=title1).first()
                #     sk.photos = image11
                #     sk.save()
                # else:
                #     messages.success(request ,"Your blog has posted successfully..!")
                #     st = Blog(title=title1, author=all11.fname, username_id = all11.id ,slug = title1, Content=Content1)
                #     st.save()
                #     sk = Blog.objects.filter(username_id = all11.id, title=title1).first()
                #     sk.photos = image11
                #     sk.save()
            else:
                messages.success(
                    request, "Your blog has posted successfully..!")
                x = Blog(title=title1, author=all11.fname,
                         username_id=all11.id, slug=title1, Content=Content1)
                x.save()
    id = request.session['person_id']
    all11 = Person.objects.filter(id=id).first()

    return render(request, 'post.html', {"all11": all11})
    # return render(request, 'post.html')


def delete_blog(request):
    url = request.META.get('HTTP_REFERER')
    if request.session.has_key('person_id'):
        u_id = request.session['person_id']
        if request.method == 'POST':
            b_id = request.POST.get('blog_id')
            if Blog.objects.filter(id=b_id, username_id=u_id):
                de = Blog.objects.get(id=b_id)
                de.delete()
                messages.success(request, "Post deleted Successfuly.......")
            else:
                messages.error(request, "you are not author..")
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


def editblog(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        all11 = request.session['person_id']
        id = request.session['person_id']
        all11 = Person.objects.filter(id=id).first()
        title1 = request.POST['name']
        Content1 = request.POST['allContent']
        image11 = request.FILES.get("image")
        # video1  = request.FILES.get("videofile")
        userslug1 = request.POST.get("postslug")
        postid1 = request.POST.get("postid")
        now = datetime.datetime.now()
        print(title1, '====', Content1, '===',
              image11, '==========', userslug1)
        post = Blog.objects.filter(id=postid1).first()
        if post.title == title1:
            x = Blog.objects.filter(id=postid1).update(Content=Content1)
            post = Blog.objects.filter(id=postid1).first()
        elif post.title != title1:
            x = Blog.objects.filter(id=postid1).update(
                title=title1, slug=title1, Content=Content1)
            post = Blog.objects.filter(id=postid1).first()
        if image11:
            sk = Blog.objects.filter(id=postid1).first()
            sk.photos = image11
            sk.save()
        # if video1:
        #     sk = Blog.objects.filter(id=postid1).first()
        #     sk.video = video1
        #     sk.save()
        messages.success(request, "Your blog has changed successfully..!")
        post = Blog.objects.filter(id=postid1).first()
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)


@csrf_protect
def editprofile(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        fname1 = request.POST.get('fname')
        lname1 = request.POST.get('lname')
        contact1 = request.POST.get('contact')
        email1 = request.POST.get('email')
        profile = request.POST.get('profile')
        bio = request.POST.get('bio')
        new = request.POST.get('postid')
        id11 = request.session['person_id']
        finding = Person.objects.filter(id=id11).update(
            fname=fname1, lname=lname1, contact=contact1, email=email1, aboutperson=profile, aboutprofile=bio)

    return HttpResponseRedirect(url)


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


def autosuggest(request):
    query_o = request.GET.get('term')
    query = Blog.objects.filter(title__icontains=query_o)
    if query:
        mylist = []
        mylist = [x.name for x in query]
        print(mylist)
        return JsonResponse(mylist, safe=False)
    else:
        e = ["No result Found!!!"]
        return JsonResponse(e, safe=False)


def Image(request):
    pid = request.session['person_id']
    if Person.objects.filter(id=pid).exists():
        if request.method == 'POST':
            p_id = request.POST.get('id')
            img = request.FILES.get('Img')
            u = Person.objects.filter(id=p_id).first()
            u.photo = img
            u.save()
            print(u.photo)
        return redirect('blog:profile')


def Likes(request):
    url = request.META.get('HTTP_REFERER')
    if request.session.has_key('person_id'):
        u_id = request.session['person_id']
        uid = Person.objects.filter(id = u_id).first()
        uid = uid.id
        if request.method == 'POST':
            bid = request.POST['like']
            if Like.objects.filter(userid=uid, blogs= bid).exists():
                c = Like.objects.get(id = lid)
                c.delete()
            else:
                c = Like(userid= bid, blogs=bid)
                c.save()
        return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)
             
 