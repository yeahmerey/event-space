
from django.contrib.admin import ModelAdmin, register
from django.http import HttpRequest

from apps.categories.models import Category


@register(Category)
class CategoryAdmin(ModelAdmin):
    """Category model admin configuration."""

    list_display = (
        "id",
        "name",
        "slug",
        "description_preview",
    )

    list_display_links = (
        "id",
        "name",
    )

    list_filter = (
        "name",
    )

    search_fields = (
        "id",
        "name",
        "slug",
        "description",
    )

    readonly_fields = (
        "id",
    )

    fields = (
        "id",
        "name",
        "slug",
        "description",
    )

    ordering = (
        "name",
    )

    list_per_page = 25
    list_max_show_all = 100

    empty_value_display = "—"

    prepopulated_fields = {
        "slug": ("name",),
    }

    save_on_top = True
    show_full_result_count = True

    @staticmethod
    def description_preview(obj: Category) -> str:
        """Return a short description for the list page."""
        if not obj.description:
            return "—"

        if len(obj.description) > 60:
            return f"{obj.description[:60]}..."

        return obj.description

    description_preview.short_description = "Description"

    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: Category | None = None,
    ) -> tuple[str, ...]:
        """Make the slug read-only after the object is created."""
        if obj:
            return self.readonly_fields + ("slug",)

        return self.readonly_fields
