from django.contrib import admin

from .models import Story, StoryLine


class StoryLineAdmin(admin.TabularInline):
    model = StoryLine


class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'posted_on']
    inlines = [
        StoryLineAdmin
    ]

admin.site.register(Story, StoryAdmin)
