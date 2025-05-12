from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status
from tutorial.quickstart.serializers import UserSerializer

from permissions import IsOwnerOrReadOnly
from .models import UserInfo, UserFollow, UserNotInterested
from .serializers import UserInfoSerializer, FollowSerializer, NotInterestedSerializer
import string
from accounts.serializers import UserReadSerializer
from django.db.models import Q
from paginations import CustomPagination


class UserInfoView(APIView):
    serializer_class = UserInfoSerializer

    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def get(self, request, id):
        user = self.user_model.objects.filter(pk=id)
        if user.exists():

            if user.first().is_staff:
                return Response({"error": 'اجازه دسترسی وجود ندارد.'}, status.HTTP_403_FORBIDDEN)

            user_info = UserInfo.objects.get(user=user.first())
            ser_data = UserInfoSerializer(instance=user_info).data
            if request.user != user.first():
                ser_data = UserInfoSerializer(instance=user_info, context={
                    'hide_field': ['following_count']}).data

            return Response(ser_data, status=status.HTTP_200_OK)
        return Response({'error': 'کاربر پیدا نشد.'}, status=status.HTTP_404_NOT_FOUND)


class UsernameUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def put(self, request):
        if request.data['username']:
            for v in request.data['username']:
                if v in string.punctuation or v == ' ':
                    return Response({"error": 'نام کاربری نمیتواند کاراکتر خاص یا فاصله داشته باشد'},
                                    status=status.HTTP_400_BAD_REQUEST)
            user = self.user_model.objects.filter(name=request.data['username'])
            if user.exists():
                return Response({'error': 'نام درخواستی گرفته شده است.'}, status=status.HTTP_400_BAD_REQUEST)
            request.user.name = request.data['username']
            request.user.save()
            return Response({'name': request.user.name, }, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'نام کاربری لازم است.'}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = UserInfoSerializer

    def put(self, request):
        try:
            user_info = UserInfo.objects.get(user=request.user)
        except UserInfo.DoesNotExist:
            return Response({'error': 'اطلاعات کاربر پیدا نشد.'}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, user_info)
        serializer = UserInfoSerializer(instance=user_info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchUserView(APIView):
    serializer_class = UserReadSerializer

    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def get(self, request, user_name):
        user_name = user_name.strip()
        if len(user_name) < 3:
            return Response({"error": 'اسم باید بیشتر از سه حرف باشد'}, status=status.HTTP_400_BAD_REQUEST)
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
        try:
            user = self.user_model.objects.get(pk=user_id, is_admin=False)
        except self.user_model.DoesNotExist:
            return Response(
                {"error": "کاربر مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.user == user:
            return Response({"error": "نمیتوانی خودت رو دنبال کنی"}, status=status.HTTP_403_FORBIDDEN)
        follow = UserFollow.objects.filter(follower=request.user, following=user)
        if follow.exists():
            follow.delete()
        else:
            UserFollow.objects.create(follower=request.user, following=user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class IsFollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), id=user_id)
        following = UserFollow.objects.filter(follower=request.user, following=user)
        return Response({"is_follow": following.exists()}, status=status.HTTP_200_OK)


class FollowersView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    def get(self, request):
        followers = UserFollow.objects.filter(following=request.user, follower__is_admin=False)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(followers, request)
        data = FollowSerializer(page, context={"hide_field": ['following', 'following_image', 'following_user_id']},
                                many=True).data
        return paginator.get_paginated_response(data)


class FollowingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    def get(self, request):
        followers = UserFollow.objects.filter(follower=request.user, following__is_admin=False)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(followers, request)
        data = FollowSerializer(page, context={"hide_field": ['follower', 'follower_user_id', 'follower_image']},
                                many=True).data
        return paginator.get_paginated_response(data)


class ToggleNotInterestedUserView(APIView):
    permission_classes = [IsAuthenticated]
    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def get(self, request, user_id):
        try:
            user = self.user_model.objects.get(pk=user_id, is_admin=False)
        except self.user_model.DoesNotExist:
            return Response(
                {"error": "کاربر مورد نظر پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.user == user:
            return Response({"error": "نمیتوانی خودت را بلاک کنی."}, status=status.HTTP_403_FORBIDDEN)
        not_interested = UserNotInterested.objects.filter(user=request.user, not_interested=user)
        if not_interested.exists():
            not_interested.delete()
        else:
            UserNotInterested.objects.create(user=request.user, not_interested=user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotInterestedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotInterestedSerializer
    def get(self, request):
        not_interested_qs = UserNotInterested.objects.filter(user=request.user, not_interested__is_admin=False)
        paginator = CustomPagination()
        page = paginator.paginate_queryset(not_interested_qs, request)
        data = NotInterestedSerializer(page, many=True).data
        return paginator.get_paginated_response(data)


class IsNotinterestedUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), id=user_id, is_admin=False)
        exists = UserNotInterested.objects.filter(user=request.user, not_interested=user).exists()
        return Response({"is_not_interested": exists}, status=status.HTTP_200_OK)
