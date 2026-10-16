from django.contrib import admin
from .models import Review, ReviewReply

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "user", "rating", "created_at")
    search_fields = ("event__title", "user__email", "comment")
    list_filter = ("rating", "created_at")

@admin.register(ReviewReply)
class ReviewReplyAdmin(admin.ModelAdmin):
    list_display = ("id", "review", "author", "created_at")
    search_fields = ("review__event__title", "author__email", "content")
    list_filter = ("created_at",)
