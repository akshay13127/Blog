from django.db import models
from user.models import User
from taggit.managers import TaggableManager
# Create your models here.


class Person(models.Model):
    #id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='person')
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    # userslug = models.CharField(max_length=50,unique=True)
    aboutperson = models.CharField(max_length=500,default='',blank=True)
    contact = models.CharField(max_length=15)
    # email = models.EmailField(max_length=50,unique=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    dateofbirth = models.DateField(null=True, blank=True)
    zipcode = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    # password = models.CharField(max_length=30)
    aboutprofile = models.CharField(max_length=500, default="", blank=True, null=True)
    photo = models.ImageField(upload_to='profile/image', default="")
    timeStamp1 = models.DateTimeField(auto_now_add=True)
    last_login= models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.fname+' '+self.lname
    
    class Meta:
        '''
        to set table name in database
        '''
        db_table = "person"


# class TokenData(models.Model):
#     user=models.OneToOneField(Person,related_name='token',blank=True,null=True,on_delete=models.CASCADE)
#     token=models.CharField( max_length=500,null=True,blank=True)
#     creationtime=models.DateTimeField(auto_now_add=True)


class Blog(models.Model):
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=200,unique=True)
    author = models.CharField(max_length=50)
    slug = models.CharField(max_length=130, unique=True)
    Content = models.TextField()
    uname = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # username = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    vieww = models.IntegerField(default=0)
    photos = models.ImageField(upload_to='blog/image/' ,default="",blank=True)
    video =  models.FileField(upload_to="blog/video/",default='',blank=True)
    rating = models.PositiveIntegerField(default=0, blank=True)    
    category = models.CharField(max_length=200)
    tags = TaggableManager()
    timeStamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    


class Like(models.Model):
    userid = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    blogs = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.userid) + str(self.blogs)


class Dislike(models.Model):
    userid = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    blogs = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.userid) + str(self.blogs)