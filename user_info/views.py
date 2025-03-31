from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status

from permissions import IsOwnerOrReadOnly
from .models import UserInfo, UserFollow
from .serializers import UserInfoSerializer, FollowSerializer
import string
from accounts.serializers import UserReadSerializer
from django.db.models import Q
from paginations import CustomPagination


class UserInfoView(APIView):
    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def get(self, request, id):
        user = self.user_model.objects.filter(pk=id)
        if user.exists():

            if user.first().is_staff:
                return Response({"error": 'permission denied'}, status.HTTP_403_FORBIDDEN)

            user_info = UserInfo.objects.get(user=user.first())
            ser_data = UserInfoSerializer(instance=user_info).data
            if request.user != user.first():
                ser_data = UserInfoSerializer(instance=user_info, context={
                    'hide_field': ['favorite_count', 'follower_count', 'following_count']}).data

            return Response(ser_data, status=status.HTTP_200_OK)
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)


class UsernameUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def put(self, request):
        if request.data['username']:
            for v in request.data['username']:
                if v in string.punctuation or v == ' ':
                    return Response({"error": 'username can not have special character or space'},
                                    status=status.HTTP_400_BAD_REQUEST)
            user = self.user_model.objects.filter(name=request.data['username'])
            if user.exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            request.user.name = request.data['username']
            request.user.save()
            return Response({'name': request.user.name, }, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, id):
        user_info = UserInfo.objects.filter(pk=id)
        if user_info.exists():
            self.check_object_permissions(request, user_info.first())
            ser_data = UserInfoSerializer(instance=user_info.first(), data=request.data, partial=True)
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'id is not found'}, status=status.HTTP_404_NOT_FOUND)


class SearchUserView(APIView):
    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def get(self, request, user_name):
        user_name = user_name.strip()
        if len(user_name) < 3:
            return Response({"error": 'username must be greater than 3 letter'}, status=status.HTTP_400_BAD_REQUEST)
        users = self.user_model.objects.filter(Q(name__icontains=user_name) & Q(is_admin=False))
        paginator = CustomPagination()
        page = paginator.paginate_queryset(users, request)
        data = UserReadSerializer(page, context={"hide_field": ['email']}, many=True).data
        return paginator.get_paginated_response(data)


class ToggleFollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def get(self, request, user_id):
        user = get_object_or_404(self.user_model, pk=user_id, is_admin=False)
        if request.user == user:
            return Response({"You cant follow yourself"}, status=status.HTTP_403_FORBIDDEN)
        follow = UserFollow.objects.filter(follower=request.user, following=user)
        if follow.exists():
            follow.delete()
        else:
            UserFollow.objects.create(follower=request.user, following=user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followers = UserFollow.objects.filter(following=request.user, follower__is_admin=False)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(followers, request)
        data = FollowSerializer(page, context={"hide_field": ['following']}, many=True).data
        return paginator.get_paginated_response(data)


class FollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        followers = UserFollow.objects.filter(follower=request.user, following__is_admin=False)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(followers, request)
        data = FollowSerializer(page, context={"hide_field": ['follower']}, many=True).data
        return paginator.get_paginated_response(data)
