from django.contrib import admin

from .models import Sentinel


@admin.register(Sentinel)
class SentinelAdmin(admin.ModelAdmin):
    list_per_page = 10
