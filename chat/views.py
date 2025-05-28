from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Message, UserChannel, Group, GroupMessage
from .serializer import ShowMessageSerializer, GroupMessageSerializer, GroupSerializer, DirectMessageSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from asgiref.sync import async_to_sync
from accounts.serializers import UserReadSerializer


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

            user_channel = UserChannel.objects.filter(user=to_user).first()
            data = {
                'type': 'receiver_function',
                'type_of_data': 'message_seen',
            }
            channel_layer = get_channel_layer()
            if user_channel:
                async_to_sync(channel_layer.send)(user_channel.channel, data)

            message = Message.objects.filter(from_user=to_user, to_user=request.user)
            message.update(has_been_seen=True)

            ser_data = ShowMessageSerializer(messages, many=True, context={"request": request}).data
            return Response(ser_data)

        except self.user_model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)




class DirectMessageGetApiView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DirectMessageSerializer
    def setup(self, request, *args, **kwargs):
        self.user_model = get_user_model()
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        user = request.user

        messages = Message.objects.filter(Q(from_user=user) | Q(to_user=user)).order_by('-date')

        user_ids = set()
        last_messages_dict = {}
        unread_counts = {}

        for msg in messages:
            other_user = msg.to_user if msg.from_user == user else msg.from_user
            user_ids.add(other_user.id)

            if other_user.id not in last_messages_dict:
                last_messages_dict[other_user.id] = msg.message

            if msg.to_user == user and not msg.has_been_seen:
                unread_counts[other_user.id] = unread_counts.get(other_user.id, 0) + 1

        users = self.user_model.objects.filter(id__in=user_ids)

        result = []
        for u in users:
            result.append({
                'id': u.id,
                'name': u.name,
                'image': u.user_info.image.url if u.user_info.image else None,
                'last_message': last_messages_dict.get(u.id, ''),
                'unread_count': unread_counts.get(u.id, 0),
            })

        return Response(result)


class GroupCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            group.members.add(request.user)
            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = Group.objects.filter(members=request.user)
        serializer = GroupSerializer(groups, many=True,context={"request": request})
        return Response(serializer.data)


class GroupAddMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id, members=request.user)
        user_ids = request.data.get('members', '').split(',')
        for user_id in user_ids:
            group.members.add(user_id)
        return Response({'detail': 'اعضا اضافه شدند.'}, status=status.HTTP_200_OK)


class GroupMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        if request.user not in group.members.all():
            return Response({'error': 'شما عضو این گروه نیستید.'}, status=status.HTTP_403_FORBIDDEN)
        messages = GroupMessage.objects.filter(group=group).order_by('date')
        serializer = GroupMessageSerializer(messages, many=True)
        return Response(serializer.data)


class GroupMembersView(APIView):
    def get(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        if request.user not in group.members.all():
            return Response({'error': 'شما عضو این گروه نیستید.'}, status=status.HTTP_403_FORBIDDEN)
        members = group.members.all()
        ser_data = UserReadSerializer(members, many=True)
        return Response({"members":ser_data.data })