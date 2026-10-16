from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Event(models.Model):
    """main event information model"""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    title = models.CharField(max_length=200)
    description = models.TextField()

    organizer = models.ForeignKey (
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="organized_events",
    )

    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.PROTECT,
        related_name="events",
    )

    venue = models.ForeignKey(
        "venues.Venue",
        on_delete=models.PROTECT,
        related_name="events",
    )

    starts_at = models.DateTimeField()

    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-starts_at"]

    def clean(self) -> None:
        super().clean()

        if (
            self.status == self.Status.PUBLISHED
            and self.starts_at
            and self.starts_at < timezone.now()
        ):
            raise ValidationError({
                "starts_at": "Published events must start in the future."
            })

        if self.venue_id and self.capacity is not None:
            if self.capacity > self.venue.capacity:
                raise ValidationError({
                    "capacity": "Event capacity cannot exceed venue capacity."
                })

    def get_absolute_url(self) -> str:
        return reverse("events:detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.title

class EventImage(models.Model):
    """image attached to an event"""
    
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(upload_to="events_images/")

    caption = models.CharField(max_length=200, blank=True)

    def __str__(self)-> str:
        return f"Image for {self.event.title}"

class EventSchedule(models.Model):
    """An activity in the event program"""
    
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="schedules",
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    class Meta:
        ordering = ["starts_at"]

    def clean(self) -> None:
        super().clean()

        if (
            self.starts_at
            and self.ends_at
            and self.ends_at <= self.starts_at
        ):
            raise ValidationError({
                "ends_at": "End time must be later than start time."
            })

    def __str__(self)-> str:
        return self.title
