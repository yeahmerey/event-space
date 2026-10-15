from django.contrib import admin

from .models import Registration, Ticket

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("id","user", "event", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user__email", "event__title")

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "registration", "code", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("code", "registration__user__email")
    readonly_fields = ("code",)