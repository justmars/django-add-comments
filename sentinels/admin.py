from django.contrib import admin

from .models import Sentinel, SentinelSlugged


@admin.register(Sentinel)
class SentinelAdmin(admin.ModelAdmin):
    list_per_page = 10


@admin.register(SentinelSlugged)
class SentinelSluggedAdmin(admin.ModelAdmin):
    list_per_page = 10
