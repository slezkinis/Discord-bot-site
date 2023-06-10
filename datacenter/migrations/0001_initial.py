# Generated by Django 4.2.2 on 2023-06-10 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick_name', models.CharField(max_length=30, verbose_name='Ник пользователя')),
                ('karma', models.IntegerField(default=0, verbose_name='Карма')),
            ],
        ),
    ]
