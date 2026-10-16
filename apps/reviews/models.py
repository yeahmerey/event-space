from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    event = models.ForeignKey(
        "events.Event", on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "event"], name="unique_review_user_event"
            )
        ]

    def clean(self):
        super().clean()
        if not self.user_id or not self.event_id:
            return
        from apps.events.models import Event
        from apps.registrations.models import Registration

        errors = {}

        if self.event.status != Event.Status.COMPLETED:
            errors["event"] = "Not possible to comment on an incomplete event."

        attended = Registration.objects.filter(
            user_id=self.user_id,
            event_id=self.event_id,
            status=Registration.Status.ATTENDED,
        ).exists()

        if not attended:
            errors["user"] = "Only users who attended the event can leave a review."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.title} - {self.user.email}: {self.rating}/5"


class ReviewReply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_replies",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def clean(self):
        super().clean()

        if not self.review_id or not self.author_id:
            return

        if self.author_id != self.review.event.organizer_id:
            raise ValidationError(
                {"author": "Only the event organizer can reply to reviews."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reply by {self.author.email} to review #{self.review_id}"
