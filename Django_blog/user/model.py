# from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractUser

# class UserManager(BaseUserManager):

#    def create_user(self, email, password=None):
#         """
#         Create and return a `User` with an email, username and password.
#         """
#         if not email:
#             raise ValueError('Users Must Have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#         )
#         if password:
#             user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password):
#         """
#         Create and return a `User` with superuser (admin) permissions.
#         """
#         if password is None:
#             raise TypeError('Superusers must have a password.')

#         user = self.create_user(email, password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()

# ROLES = (
#     ('employee', 'Employee'),
#     ('employer', 'Employer')
# )


# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True, blank=False, null=False,)
#     role = models.CharField(max_length=10, choices=ROLES)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects: UserManager()
#     def __str__(self):
#         return self.email

#     def __unicode__(self):
#         return self.email

#     def get_context(self, obj=None):
#         if self.is_active and self.is_superuser:
#             queryset = 
        
# def pattern(a):
#     rows = a
#     i = 1
#     while i <= rows:
#         j = 1
#         while j <= i:
#             print(( i * 2 -1), end =" ")
#             j +=1 
#         i += 1
#         print()
    

# pattern(5)



a = [1,2,0,34,54,4,90,2,8]


# for i in range(len(a)):
#     for j in range(i+1,len(a)):
#         if a[i] > a[j]:
# #             a[i], a[j] = a[j], a[i]
# # print(a)

# def fact(n):
#     if n == 1:
#         return n
#     else:
#         # return n
#         return fact( * fact(n-1)


# n= 5
# if n < 0:
#     print(n)
# else:
#     print(fact(n))


# a = [i*i for i in a]
# print (a)

class A():
    def fuc(self):
        print( "Class Method")

a = A()

a.fuc()




