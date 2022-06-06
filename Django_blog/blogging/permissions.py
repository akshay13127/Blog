 
from rest_framework.permissions import BasePermission, SAFE_METHODS
from user.models import User
from rest_framework_jwt.settings import api_settings

JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object.'
    # my_safe_method = ['GET', 'PUT']
    # def has_permission(self, request, view):
    #     if request.method in self.my_safe_method:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        #member = Membership.objects.get(user=request.user)
        #member.is_active
        if request.method in SAFE_METHODS:
            return True
        return obj.id == request.session['person_id']

class TokenRequired(BasePermission):

    def has_permission(self, request, view, *args, **kwargs):
        # print(request.headers.get('Authentication'))
        print("gdhfgkahfgdhkagsfkhagfhgaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaashdaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        # a = request.headers.get('Authentication')
        # a = args[0].headers.get('Authorization')
        a = request.headers.get('Authorization')
        token_obj = a.split(" ")[1]
        d_token = JWT_DECODE_HANDLER(token_obj)
        print('@@@@@@@@@@@@@', d_token)
        if User.objects.filter(id = d_token['user_id']).exists():
        # if self.d_token:
            print("chall raha hai bhai paresan mt ho")
            return True
        else:
            print("bhot baddi paresani hai bhai",user_obj)
            return False
        # return True