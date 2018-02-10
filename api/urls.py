from django.conf.urls import url
from api.views import *

urlpatterns = [
    url(r'^list/$', MyfeedListAPIView.as_view(), name="list"),
    url(r'^detail/(?P<myfeed_id>[0-9]+)/$', MyfeedDetailAPIView.as_view(), name="detail"),
    url(r'^update/(?P<myfeed_id>[0-9]+)/$', MyfeedUpdateAPIView.as_view(), name="update"),
    url(r'^delete/(?P<myfeed_id>[0-9]+)/$', MyfeedDeleteAPIView.as_view(), name="delete"),
    url(r'^create/$', MyfeedCreateAPIView.as_view(), name="create"),

  

    url(r'^register/$', UserCreateAPIView.as_view(), name="register"),
    url(r'^login/$', UserLoginAPIView.as_view(), name="login"),


]