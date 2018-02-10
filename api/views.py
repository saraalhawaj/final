
# from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
# from main.models import *

# from .serializers import (
# 	MyfeedListSerializer,
# 	MyfeedDetailSerializer,
# 	MyfeedCreateSerializer,
	
# 	UserCreateSerializer,
# 	UserLoginSerializer,
# 	)

# from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
# from .permissions import IsOwner
# from rest_framework.filters import SearchFilter, OrderingFilter
# from django.db.models import Q
# # from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import User
# from django.utils import timezone

# from rest_framework.response import Response
# from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
# from rest_framework.views import APIView

# class UserCreateAPIView(CreateAPIView):
# 	queryset = CustomUser.objects.all()
# 	serializer_class = UserCreateSerializer

# class UserLoginAPIView(APIView):
# 	permission_classes = [AllowAny]
# 	serializer_class = UserLoginSerializer

# 	def Myfeed(self, request, format=None):
# 		data = request.data
# 		serializer = UserLoginSerializer(data=data)
# 		if serializer.is_valid(raise_exception=True):
# 			new_data = serializer.data
# 			return Response(new_data, status=HTTP_200_OK)
# 		return Response(serializer.errors, HTTP_400_BAD_REQUEST)


# # class MyfeedListAPIView(ListAPIView):
# # 	queryset = Myfeed.objects.all()
# # 	serializer_class = MyfeedListSerializer
# # 	permission_classes = [AllowAny]
# # 	# pagination_class = PageNumberPagination

# # 	def get_queryset(self, *args, **kwargs):
# # 		queryset_list = Myfeed.objects.all()
# # 		query = self.request.GET.get("q")
# # 		if query:
# # 			queryset_list = queryset_list.filter(
# # 				Q(username__icontains=query)|
# # 				Q(book__icontains=query)|
# # 				Q(feed__first_name__icontains=query)
# # 				).distinct()
# # 		return queryset_list

# # class MyfeedDetailAPIView(RetrieveAPIView):
# # 	queryset = Myfeed.objects.all()
# # 	serializer_class = MyfeedDetailSerializer
# # 	permission_classes = [AllowAny]
	

# # class MyfeedDeleteAPIView(DestroyAPIView):
# # 	queryset = Myfeed.objects.all()
# # 	serializer_class = MyfeedDetailSerializer
# # 	permission_classes = [IsAuthenticated, IsAdminUser]
	

# # class MyfeedCreateAPIView(CreateAPIView):
# # 	queryset = Myfeed.objects.all()
# # 	serializer_class = MyfeedCreateSerializer
# # 	permission_classes = [IsAuthenticated, IsAdminUser]

# # 	def perform_create(self, serializer):
# # 		serializer.save(author=self.request.user)


# # class MyfeedUpdateAPIView(RetrieveUpdateAPIView):
# # 	queryset = Myfeed.objects.all()
# # 	serializer_class = MyfeedCreateSerializer
# # 	permission_classes = [IsAuthenticated, IsOwner]
# # 	
from .serializers import MyfeedListSerializer
from rest_framework.generics import RetrieveAPIView
from .serializers import MyfeedDetailSerializer,UserCreateSerializer, ReplyCreateSerializer
from rest_framework.generics import DestroyAPIView
from rest_framework.generics import CreateAPIView,ListAPIView
from .serializers import MyfeedCreateSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from main.models import *
from .serializers import UserCreateSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwner

from .serializers import UserLoginSerializer
from .serializers import UserCreateSerializer
from rest_framework.filters import SearchFilter

class MyfeedListAPIView(ListAPIView):
    serializer_class = MyfeedListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['course', 'feed', 'book','major']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Myfeed.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(feed__icontains=query)|
                Q(book__icontains=query)
                ).distinct()
        return queryset_list
class UserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
class MyfeedCreateAPIView(CreateAPIView):
    queryset = Myfeed.objects.all()
    serializer_class = MyfeedCreateSerializer


class ReplyCreateAPIView(CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplyCreateSerializer
    
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class MyfeedDetailAPIView(RetrieveAPIView):

    serializer_class = MyfeedDetailSerializer
    permission_classes = [AllowAny]
    

class MyfeedDeleteAPIView(DestroyAPIView):
    queryset = Myfeed.objects.all()
    serializer_class = MyfeedDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
   

# class MyfeedCreateAPIView(CreateAPIView):
#     queryset = Myfeed.objects.all()
#     serializer_class = MyfeedCreateSerializer
#     permission_classes = [IsAuthenticated, IsAdminUser]

#     def perform_create(self, serializer):
#         serializer.save(username=self.request.user)



class MyfeedUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Myfeed.objects.all()
    serializer_class = MyfeedCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner]
