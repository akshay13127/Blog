from rest_framework import routers, serializers, viewsets
 
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )
from .models import Person, Blog
from user.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class PersonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['fname', 'lname', 'email', 'contact', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['fname', 'lname', 'contact', 'aboutperson', 'aboutprofile','photo']


class PersonListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    class Meta:
        model = Person
        fields = ['email', 'password',]

        extra_kwargs = {'password': {'write_only': True}}
    # def to_representation(self, instance):
    #     rep = super(PersonSerializer, self).to_representation(instance)
    #     rep['author_name'] = instance.username.fname +" " +instance.username.lname
    #     return rep

class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True)
    # username = CharField()
    email = EmailField(label='Email Address')
    class Meta:
        model = Person
        fields = [
            'email',
            'password',
            'token',
            
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                            }
    def validate(self, data):

        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError("This user has already registered.")
        return data



post_detail_url = HyperlinkedIdentityField(view_name='blogg:detail', lookup_field='slug')
person_detail_url = HyperlinkedIdentityField(view_name='blogg:profile', lookup_field='pk')

class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = PersonSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(PostListSerializer, self).to_representation(instance)
        # rep['author_name'] = instance.person.fname +" " +instance.person.lname
        return rep
    
class CreatePostSerializer(ModelSerializer):
    # url = post_detail_url
    user = PersonSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'

class PostUpdateSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    # comments = SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(PostDetailSerializer, self).to_representation(instance)
        # rep['author_name'] = instance.username.fname +" " +instance.username.lname
        # rep['author_pic'] = instance.username.photo
        return rep
    

class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    # comments = SerializerMethodField()
    
    class Meta:
        model = Blog
        fields = "__all__"
    
    def to_representation(self, instance):
        rep = super(PostDetailSerializer, self).to_representation(instance)
        # rep['author_name'] = instance.username.fname +" " +instance.username.lname
        # rep['author_pic'] = instance.username.photo
        return rep
    

    def get_html(self, obj):
        try:
            obj1 = obj.get_markdown()
        except:
            obj1 = None
        return obj1

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image


class ProfileDetailSerializer(ModelSerializer):
    # url = person_detail_url
    # user = UserDetailSerializer(read_only=True)
    # image = SerializerMethodField()
    # html = SerializerMethodField()
    # # comments = SerializerMethodField()
    
    class Meta:
        model = User
        fields = "__all__"

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            #'id',
            'title',
            #'slug',
            'Content',
            'timeStamp'
        ]










class changep(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"email", 'password']
        read_only = ['id',"email"]
    # def update(self, instance, validated_data):
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.save()
    #     return instance
   