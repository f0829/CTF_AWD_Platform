from django.shortcuts import render

# Create your views here.



from .serializers import UserSerializer
from .models import UserProfile
from rest_framework import mixins,generics
from rest_framework import viewsets
from rest_framework.authentication import BaseAuthentication  #基础验证。必须重写其中的方法
from rest_framework.permissions import IsAuthenticated,IsAdminUser  #直接调用
from rest_framework import permissions
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

# Create your views here.

class MyAuth(BaseAuthentication):
    '''
    自定义认证
    '''
    def authenticate(self, request):
        pass
    def authenticate_header(self, request):
        pass


class UserPermission(permissions.BasePermission):
    '''
    自定义权限判断
    '''
    message = '您无权使用该请求'
    def has_object_permission(self, request, view, obj):
        '''
        object级别权限（后判断这个）
        :param request:
        :param view:
        :param obj:
        :return:
        '''
        print(obj)
        print(dir(obj))
        print('ssss')
        if bool(request.user and request.user.is_authenticated):
            print('1')
            if request.method in ('GET', 'HEAD', 'OPTIONS','PUT'):
                return True
            elif request.user.is_superuser:
                return True
            else:
                return False
        else:
            return False

    def has_permission(self, request, view):
        '''
        model 级别权限（先判断这个）
        :param request:
        :param view:
        :return:
        '''
        if bool(request.user and request.user.is_authenticated):
            if request.method in ('GET', 'HEAD', 'OPTIONS', 'PUT'):
                return True
            elif request.user.is_superuser:
                return True
            else:
                return False
        else:
            return False

class UserFilter(django_filters.rest_framework.FilterSet):
    '''
    None
    '''
    # def filter_queryset(self, request, queryset, view):
    #     if request.user.is_superuser:
    #         # print(True)
    #         return queryset
    #     else:
    #         return queryset.filter(username=request.user)

    class Meta:
        model = UserProfile
        fields = ['id']


class UserProfilePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 50


class UserProfileView(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    pagination_class = UserProfilePagination   #   warining #20
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    permission_classes = (UserPermission,)

    # filter_backends = (UserFilter,)
    # ordering = ('id',)

    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = UserFilter

    ordering_fields = ('id',)
    search_fields = ('=username', '=id')  # 搜索指定字段，支持多种搜索模式
    # filterset_fields = ('username','id')  #http://127.0.0.1:8000/api/user/?username=admin

    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('=username','=id')  #搜索指定字段，支持多种搜索模式

    # filter_backends = (filters.OrderingFilter,)   #排序过滤
    # ordering_fields = ('username','id')




# from rest_framework.views import APIView
# from rest_framework.authentication import SessionAuthentication,BasicAuthentication
# from rest_framework.response import Response
# class TestView(APIView):
#     authentication_classes = (SessionAuthentication,BasicAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     def get(self,request,format=None):
#         content = 'testview'
#         return Response(content)









