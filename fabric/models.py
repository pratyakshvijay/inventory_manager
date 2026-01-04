from django.db import models # type: ignore

class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class FabricLot(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=100)
    fabric_type = models.CharField(max_length=100)
    gst = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    lot_number = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.lot_number} - {self.fabric_type}"

    def total_meters(self):
        return sum(color.meter for color in self.colors.all())

    def total_amount(self):
        base_amount = self.total_meters() * self.rate
        discounted = base_amount - self.discount
        return discounted + (discounted * self.gst / 100)


class FabricColorDetail(models.Model):
    lot = models.ForeignKey(FabricLot, related_name="colors", on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    meter = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.color} ({self.meter} m)"

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class JobWorkIssue(models.Model):
    issue_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Issue {self.issue_number} - {self.manufacturer.name}"


class JobWorkFabricItem(models.Model):
    issue = models.ForeignKey(JobWorkIssue, related_name='items', on_delete=models.CASCADE)
    fabric_lot = models.ForeignKey('FabricLot', on_delete=models.CASCADE)
    color_detail = models.ForeignKey('FabricColorDetail', on_delete=models.CASCADE)
    meter_issued = models.FloatField()

    def __str__(self):
        return f"{self.color_detail.color} - {self.meter_issued} m"
    
class JobWorkFabricItemSize(models.Model):
    fabric_item = models.ForeignKey(JobWorkFabricItem, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=10)  # e.g. '28', '30', '32'
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.fabric_item.color_detail.color} - Size {self.size} ({self.quantity})"
