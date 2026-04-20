from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'active', 'created_at')
    list_editable = ('active',)
    search_fields = ('text',)
