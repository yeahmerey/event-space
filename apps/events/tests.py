
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.categories.models import Category
from apps.venues.models import Venue

from .models import Event, EventImage, EventSchedule


class EventTests(TestCase):
    def setUp(self) -> None:
        user_model = get_user_model()

        self.organizer = user_model(
            email="organizer@example.com",
            first_name="Test",
            last_name="Organizer",
        )
        self.organizer.set_password("TestPassword123!")
        self.organizer.save()

        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
        )

        self.venue = Venue.objects.create(
            name="KBTU Conference Hall",
            address="Tole Bi 59",
            city="Almaty",
            capacity=200,
        )

        self.event = Event.objects.create(
            title="AI Conference",
            description="Artificial Intelligence Conference",
            organizer=self.organizer,
            category=self.category,
            venue=self.venue,
            starts_at=timezone.now() + timedelta(days=7),
            capacity=100,
            status=Event.Status.PUBLISHED,
        )

    def test_event_creation(self) -> None:
        self.assertEqual(self.event.title, "AI Conference")
        self.assertEqual(self.event.category, self.category)

    def test_venue_capacity_validation(self) -> None:
        self.event.capacity = 300

        with self.assertRaises(ValidationError):
            self.event.full_clean()

    def test_event_list(self) -> None:
        response = self.client.get(
            reverse("events:list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI Conference")

    def test_anonymous_cannot_create_event(self) -> None:
        response = self.client.get(
            reverse("events:create")
        )

        self.assertEqual(response.status_code, 302)

    def test_other_user_cannot_edit_event(self) -> None:
        user_model = get_user_model()

        other_user = user_model(
            email="other@example.com",
            first_name="Other",
            last_name="User",
        )
        other_user.set_password("OtherPassword123!")
        other_user.save()

        self.client.force_login(other_user)

        response = self.client.get(
            reverse(
                "events:update",
                kwargs={"pk": self.event.pk},
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_schedule_validation(self) -> None:
        start = timezone.now()

        schedule = EventSchedule(
            event=self.event,
            title="Opening",
            starts_at=start,
            ends_at=start - timedelta(hours=1),
        )

        with self.assertRaises(ValidationError):
            schedule.full_clean()

    def test_event_image(self) -> None:
        image = EventImage.objects.create(
            event=self.event,
            image="events/images/test.jpg",
            caption="Conference Photo",
        )

        self.assertEqual(image.event, self.event)
        self.assertEqual(self.event.images.count(), 1)

