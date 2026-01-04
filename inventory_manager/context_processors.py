from .models import SKU
from django.db.models import Sum

def total_stock_context(request):
    total = SKU.objects.aggregate(total=Sum('stock_quantity'))['total'] or 0
    low_stock_count = SKU.objects.filter(stock_quantity__lt=10).count()
    return {
        'total_stock': total,
        'low_stock_count': low_stock_count
    }
