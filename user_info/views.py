from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import status
from permissions import IsOwnerOrReadOnly
from .models import UserInfo
from .serializers import UserInfoSerializer

class UserInfoView(APIView):
    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def get(self, request,id):
        user = self.user_model.objects.filter(pk=id)
        if user.exists():
            user_info = UserInfo.objects.get(user=user.first())
            ser_data = UserInfoSerializer(instance=user_info).data
            return Response(ser_data, status=status.HTTP_200_OK)
        return Response({'error':'user not found'},status=status.HTTP_404_NOT_FOUND)


class UsernameUpdateView(APIView):

    permission_classes = [IsAuthenticated]
    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)


    def put(self, request):
        if request.data['username']:
            user = self.user_model.objects.filter(name=request.data['username'])
            if user.exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            request.user.name = request.data['username']
            request.user.save()
            return Response({'name': request.user.name,}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    def put(self, request,id):
        user_info = UserInfo.objects.filter(pk=id)
        self.check_object_permissions(request, user_info.first())
        if user_info.exists():
            ser_data = UserInfoSerializer(instance=user_info.first(),data=request.data,partial=True)
            if ser_data.is_valid():
                ser_data.save()
                return Response(ser_data.data, status=status.HTTP_200_OK)
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'id is not found'}, status=status.HTTP_404_NOT_FOUND)