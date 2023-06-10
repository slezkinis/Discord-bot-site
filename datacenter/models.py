from django.db import models


class DiscordUser(models.Model):
    nick_name = models.CharField('Ник пользователя', max_length=30)
    karma = models.IntegerField('Карма', default=0)

    def __str__(self) -> str:
        return self.nick_name