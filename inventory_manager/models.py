from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class SyncLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="completed")
    synced_items = models.PositiveIntegerField(default=0)
    product_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} synced {self.synced_items} items @ {self.timestamp.strftime('%d-%b %H:%M')}"

class SKU(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sku_code = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=255)
    stock_quantity = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku_code} - {self.product_name}"
    
class ChannelListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, default="Flipkart")
    channel_sku = models.CharField(max_length=100, unique=True)  # Flipkart SKU
    fsn = models.CharField(max_length=100)
    master_sku = models.ForeignKey(SKU, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.channel_sku} → {self.master_sku.sku_code if self.master_sku else 'Unmapped'}"


class InventoryTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    SOURCE_CHOICES = [
        ('manual', 'Manual'),
        ('excel', 'Excel Upload'),
        ('flipkart_order', 'Flipkart Order File'),
        ('api_sync', 'Flipkart API Sync'),
    ]

    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    quantity_change = models.IntegerField()
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sign = '+' if self.quantity_change >= 0 else ''
        return f"{self.timestamp.date()} | {self.sku.sku_code} | {sign}{self.quantity_change} ({self.source})"

class FlipkartInventorySnapshot(models.Model):
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    flipkart_quantity = models.IntegerField()
    synced_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sku.sku_code} - {self.flipkart_quantity} @ {self.synced_at}"

class Bag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bag_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reflect_in_rack = models.BooleanField(default=False)

    def __str__(self):
        return self.bag_number

class BagItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE, related_name='items')
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    product_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.bag.bag_number} - {self.sku.sku_code} ({self.quantity})"

class Rack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    sku = models.OneToOneField(SKU, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sku.sku_code} - {self.quantity}"
