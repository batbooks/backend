from django.db import models
from django.contrib.auth import get_user_model


class Message(models.Model):
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='to_user')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    has_been_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.from_user} -> {self.to_user} : {self.message}'


class UserChannel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='channel_user')
    channel = models.TextField()

    def __str__(self):
        return f'{self.user} -> {self.channel}'

class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(get_user_model(), related_name='groups')

    def __str__(self):
        return self.name


class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} -> {self.group.name}: {self.message}'
