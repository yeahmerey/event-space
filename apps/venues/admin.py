
from django.contrib.admin import ModelAdmin, register
from django.http import HttpRequest

from apps.venues.models import Venue


@register(Venue)
class VenueAdmin(ModelAdmin):
    """Venue model admin configuration."""

    list_display = (
        "id",
        "name",
        "city",
        "address",
        "capacity",
        "is_active",
        "created_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    list_filter = (
        "city",
        "is_active",
        "created_at",
    )

    search_fields = (
        "id",
        "name",
        "address",
        "city",
    )

    readonly_fields = (
        "id",
        "created_at",
    )

    fields = (
        "id",
        "name",
        "address",
        "city",
        "capacity",
        "is_active",
        "created_at",
    )

    ordering = (
        "city",
        "name",
    )

    list_per_page = 25
    list_max_show_all = 100

    empty_value_display = "—"

    list_editable = (
        "is_active",
    )

    save_on_top = True
    show_full_result_count = True

    actions_on_top = True
    actions_on_bottom = True

    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: Venue | None = None,
    ) -> tuple[str, ...]:
        """Return fields that cannot be edited."""
        return self.readonly_fields
