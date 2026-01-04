from django.db.models import Sum
from .models import SKU

def total_stock_context(request):
    if not request.user.is_authenticated:
        return {
            'total_stock': 0,
            'low_stock_count': 0,
        }

    skus = SKU.objects.filter(user=request.user)

    total = skus.aggregate(total=Sum('stock_quantity'))['total'] or 0
    low_stock_count = skus.filter(
        stock_quantity__lt=10,
        stock_quantity__gt=0
    ).count()

    return {
        'total_stock': total,
        'low_stock_count': low_stock_count
    }
