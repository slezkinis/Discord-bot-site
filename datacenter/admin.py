from django.contrib import admin
from .models import DiscordUser

@admin.register(DiscordUser)
class DiscordUserAdmin(admin.ModelAdmin):
    pass