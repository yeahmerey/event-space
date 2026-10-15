from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Venue(models.Model):
    name = models.CharField(max_length=150,)
    address = models.CharField(max_length=255,)
    city = models.CharField(max_length=100,)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)], )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ["city", "name"]
        constraints= [ models.UniqueConstraint(fields=["name", "address", "city"], name="unique_venue_location")]

    def __str__(self):
        return f"{self.name}, {self.city}"

