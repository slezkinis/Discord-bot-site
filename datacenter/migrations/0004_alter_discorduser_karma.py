# Generated by Django 4.2.2 on 2023-06-10 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0003_alter_discorduser_karma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discorduser',
            name='karma',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Карма'),
        ),
    ]
