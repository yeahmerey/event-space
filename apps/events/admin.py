
from django.contrib import admin

from .models import Event, EventImage, EventSchedule


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1


class EventScheduleInline(admin.TabularInline):
    model = EventSchedule
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "organizer",
        "category",
        "venue",
        "starts_at",
        "capacity",
        "status",
    )

    list_filter = (
        "status",
        "category",
        "venue",
        "starts_at",
    )

    search_fields = (
        "title",
        "description",
        "organizer__email",
    )

    ordering = ("starts_at",)

    list_select_related = (
        "organizer",
        "category",
        "venue",
    )

    inlines = [
        EventImageInline,
        EventScheduleInline,
    ]


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ("event", "caption")
    search_fields = ("event__title", "caption")


@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "event",
        "starts_at",
        "ends_at",
    )

    list_filter = ("starts_at",)
    search_fields = ("title", "event__title")
    ordering = ("starts_at",)
