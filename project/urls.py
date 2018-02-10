from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls.static import static
from main import views
from django.contrib import admin
# from django.urls import path
# from chat import views
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('chat/<int:sender_id>/', views.chat),
#     path('chat_list/', views.chat_list ),
#     path('message/send/', views.messages ),
# ]


urlpatterns = [
 url('admin/', admin.site.urls),
 url(r'^api/', include('api.urls', namespace="api")),
    url(r'^profile/$', views.profile_page, name="profile"),
    url(r'^edit_profile/$', views.edit_profile, name="edit_profile"),
    url(r'chat/(?P<sender_id>[0-9]+)/$', views.chat, name="chat"),
    url(r'^chat_list/$', views.chat_list ),
    url(r'^message/send/$', views.messages ),
    
    url(r'^list/', views.myfeed_list, name="list"),
    url(r'^wishlist/', views.wish_list, name="wishlist"),
    url(r'^detail/(?P<pk>\d+)/$', views.myfeed_detail, name="detail"),

    url(r'^create/', views.myfeed_create, name="create"),
    url(r'^update/(?P<pk>\d+)/$', views.myfeed_update, name="update"),
    url(r'^delete/(?P<pk>\d+)/$', views.myfeed_delete, name="delete"),


    url(r'^signup/$', views.sign_up, name="signup"),
    url(r'^logout/', views.logout_view, name="logout"),
    url(r'^login/', views.login_view, name="login"),

    url(r'^likes/(?P<myfeed_id>[0-9]+)/$', views.likes, name="likes"),

]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

