import secrets
import string

from django.conf import settings
from django.db import models

def generate_ticket_code():
   alphabet = string.ascii_uppercase + string.digits
   return "".join(secrets.choice(alphabet) for _ in range(12))


class Registration(models.Model):
   class Status(models.TextChoices):
       ACTIVE = "active", "Active"          
       CANCELLED = "cancelled", "Cancelled"  
       ATTENDED = "attended", "Attended"     

   user = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       on_delete=models.PROTECT,
       related_name="registrations",
   )
   event = models.ForeignKey(
       "events.Event",
       on_delete=models.PROTECT,
       related_name="registrations",
   )
   status = models.CharField(
       max_length=20,
       choices=Status.choices,
       default=Status.ACTIVE,
   )
   created_at = models.DateTimeField(auto_now_add=True)

   class Meta:
       ordering = ["-created_at"]
       constraints = [
           models.UniqueConstraint(
               fields=("user", "event"),
               name="unique_user_event_registration",
           )
       ]

   def __str__(self):
       return f"{self.user} -> {self.event} ({self.status})"


class Ticket(models.Model):
   class Status(models.TextChoices):
       VALID = "valid", "Valid" 
       USED = "used", "Used"     
       VOID = "void", "Void"     

   registration = models.OneToOneField(
       Registration,
       on_delete=models.PROTECT,
       related_name="ticket",
   )
   code = models.CharField(max_length=20, unique=True, blank=True)
   status = models.CharField(
       max_length=20,
       choices=Status.choices,
       default=Status.VALID,
   )
   created_at = models.DateTimeField(auto_now_add=True)

   def save(self, *args, **kwargs):
       if not self.code:
           code = generate_ticket_code()
           while Ticket.objects.filter(code=code).exists():
               code = generate_ticket_code()
           self.code = code
       super().save(*args, **kwargs)

   def __str__(self):
       return f"Ticket {self.code} ({self.status})"