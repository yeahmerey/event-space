
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q, QuerySet
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import EventForm
from .models import Event


class EventListView(ListView):
    model = Event
    template_name = "events/event_list.html"
    context_object_name = "events"

    def get_queryset(self) -> QuerySet[Event]:
        queryset = Event.objects.filter(
            status=Event.Status.PUBLISHED
        ).select_related(
            "organizer",
            "category",
            "venue",
        )

        search = self.request.GET.get("search", "").strip()
        category = self.request.GET.get("category", "")

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        if category.isdigit():
            queryset = queryset.filter(
                category_id=int(category)
            )

        return queryset


class EventDetailView(DetailView):
    model = Event
    template_name = "events/event_detail.html"
    context_object_name = "event"

    def get_queryset(self) -> QuerySet[Event]:
        queryset = Event.objects.select_related(
            "organizer",
            "category",
            "venue",
        ).prefetch_related("images", "schedules")

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(status=Event.Status.PUBLISHED)
                | Q(organizer=self.request.user)
            )

        return queryset.filter(
            status=Event.Status.PUBLISHED
        )


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)


class OwnerRequiredMixin(LoginRequiredMixin):
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.organizer_id != self.request.user.pk:
            raise PermissionDenied(
                "Only the organizer can modify this event."
            )

        return obj


class EventUpdateView(OwnerRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/event_form.html"


class EventDeleteView(OwnerRequiredMixin, DeleteView):
    model = Event
    template_name = "events/event_confirm_delete.html"
    success_url = reverse_lazy("events:list")
