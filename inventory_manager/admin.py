from django.contrib import admin
from .models import SKU, InventoryTransaction, FlipkartInventorySnapshot

admin.site.register(SKU)
admin.site.register(InventoryTransaction)
admin.site.register(FlipkartInventorySnapshot)
