from django.db import models
from django.utils import timezone


class DiscordUser(models.Model):
    nick_name = models.CharField('Ник пользователя', max_length=30)
    karma = models.IntegerField('Карма', default=0)
    last_karma = models.DateTimeField('Последнее спасибо', default=timezone.now, db_index=True)

    def __str__(self) -> str:
        return self.nick_name