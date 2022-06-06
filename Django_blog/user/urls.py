from django.conf.urls import url
from user.views import UserRegistrationView, UserLoginView

app_name = 'newacc'

urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view(), name = 'signup'),
    url(r'^signin', UserLoginView.as_view(), name='signin'),
    ]