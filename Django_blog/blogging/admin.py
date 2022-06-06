from django.contrib import admin
from blogging.models import Person, Blog, Like, Dislike

# Register your models here.
admin.site.register(Person)
admin.site.register(Blog)
admin.site.register(Like)
admin.site.register(Dislike)

