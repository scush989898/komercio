from django.db import models
import uuid


class Product(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    description = models.TextField()
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    seller = models.ForeignKey(
        "accounts.Account",
        on_delete=models.CASCADE,
        related_name="products",
    )
