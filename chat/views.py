from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Message, UserChannel, Group, GroupMessage
from .serializer import ShowMessageSerializer,GroupMessageSerializer,GroupSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from asgiref.sync import async_to_sync


class ShowMessageApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShowMessageSerializer
    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def get(self, request, user_id):
        try:
            to_user = self.user_model.objects.get(pk=user_id)
            messages = Message.objects.filter(
                Q(from_user=request.user, to_user=to_user) | Q(from_user=to_user, to_user=request.user))

            user_channel = UserChannel.objects.get(user=request.user)
            data = {
                'type': 'receiver_function',
                'type_of_data': 'message_seen',
            }
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send)(user_channel.channel, data)

            message = Message.objects.filter(from_user=to_user, to_user=request.user)
            message.update(has_been_seen=True)

            ser_data = ShowMessageSerializer(messages, many=True).data
            return Response(ser_data)

        except self.user_model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MessageDeleteApiView(APIView):
    permission_classes = (IsOwnerOrReadOnly,)
    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        super().setup(request, *args, **kwargs)

    def delete(self, request, message_id):
        try:
            message = Message.objects.get(pk=message_id)
            self.check_object_permissions(request, message)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class GroupCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            group.members.add(request.user)  # سازنده به گروه اضافه بشه
            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = Group.objects.filter(members=request.user)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


class GroupAddMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        user_ids = request.data.get('members', [])
        for user_id in user_ids:
            group.members.add(user_id)
        return Response({'detail': 'اعضا اضافه شدند.'}, status=status.HTTP_200_OK)


class GroupMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        if request.user not in group.members.all():
            return Response({'detail': 'شما عضو این گروه نیستید.'}, status=status.HTTP_403_FORBIDDEN)
        messages = GroupMessage.objects.filter(group=group).order_by('date')
        serializer = GroupMessageSerializer(messages, many=True)
        return Response(serializer.data)