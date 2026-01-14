from django.db import models
from django.conf import settings

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)  # active, canceled, etc.
    plan_id = models.CharField(max_length=10, choices=(('30', '30 Days'), ('90', '90 Days')))
    created_at = models.DateTimeField(auto_now_add=True)
    current_period_end = models.DateTimeField()

    def __str__(self):
        return f"{self.user.email} - {self.plan_id} days"





