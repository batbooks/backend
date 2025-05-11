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


