from django import forms
from django.forms import inlineformset_factory, formset_factory, BaseInlineFormSet
from .models import JobWorkFabricItemSize, Vendor, FabricLot, FabricColorDetail, JobWorkIssue, JobWorkFabricItem, Manufacturer
from django.forms.models import ModelChoiceField
from django.db.models import Sum, F
from collections import defaultdict
from django.core.exceptions import ValidationError
from decimal import Decimal

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class FabricLotForm(forms.ModelForm):
    class Meta:
        model = FabricLot
        fields = '__all__'
        widgets = {
            'lot_number': forms.TextInput(attrs={'class': 'form-control'}),
            'vendor': forms.Select(attrs={'class': 'form-select'}),
            'invoice_no': forms.TextInput(attrs={'class': 'form-control'}),
            'fabric_type': forms.TextInput(attrs={'class': 'form-control'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'gst': forms.NumberInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

FabricColorFormSet = inlineformset_factory(
    FabricLot,
    FabricColorDetail,
    fields=['color', 'meter'],
    extra=1,
    can_delete=True
)

class JobWorkIssueForm(forms.ModelForm):
    class Meta:
        model = JobWorkIssue
        fields = ['issue_number', 'issue_date', 'manufacturer']
        widgets = {
            'issue_number': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'manufacturer': forms.Select(attrs={'class': 'form-select'}),
        }

class JobWorkFabricItemForm(forms.ModelForm):
    class Meta:
        model = JobWorkFabricItem
        fields = ['fabric_lot', 'color_detail', 'meter_issued']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            available_lots = FabricLot.objects.annotate(
                total_available=Sum('colors__meter'),
                total_issued=Sum('colors__jobworkfabricitem__meter_issued'),
            ).filter(
                total_issued__lt=F('total_available')
            ).distinct()

            class RemainingLabelChoiceField(ModelChoiceField):
                def label_from_instance(self, obj):
                    remaining = (obj.total_available or 0) - (obj.total_issued or 0)
                    return f"{obj.lot_number} ({remaining:.2f} m left)"

            self.fields['fabric_lot'] = RemainingLabelChoiceField(
                queryset=available_lots,
                widget=forms.Select(attrs={'class': 'form-control'}),
                required=False
            )

class JobWorkFabricItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        issued_tracker = defaultdict(float)

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue

            if not form.cleaned_data:
                continue

            fabric_lot = form.cleaned_data.get('fabric_lot')
            color_detail = form.cleaned_data.get('color_detail')
            meter_issued = form.cleaned_data.get('meter_issued') or 0

            if not (fabric_lot and color_detail):
                continue

            color_key = (fabric_lot.id, color_detail.id)

            # Add current row to the tracker
            issued_tracker[color_key] += meter_issued

            # Fetch available meter for this color
            available_meter = color_detail.meter

            # Calculate total issued for this color from DB
            db_issued = JobWorkFabricItem.objects.filter(
                fabric_lot=fabric_lot,
                color_detail=color_detail
            ).exclude(issue=self.instance.pk if self.instance else None
            ).aggregate(total=Sum('meter_issued'))['total'] or 0

            remaining = float(available_meter) - db_issued

            # Validate
            if issued_tracker[color_key] > remaining:
                raise ValidationError(
                    f"Cannot issue {issued_tracker[color_key]} m for {color_detail.color} in {fabric_lot.lot_number}. Only {remaining:.2f} m available."
                )

JobWorkFabricItemFormSet = inlineformset_factory(
    JobWorkIssue,
    JobWorkFabricItem,
    formset=JobWorkFabricItemFormSet,  # this is the custom one
    fields=('fabric_lot', 'color_detail', 'meter_issued'),
    extra=1,
    can_delete=True
)

class JobWorkFabricItemSizeForm(forms.ModelForm):
    class Meta:
        model = JobWorkFabricItemSize
        fields = ['size', 'quantity']
        widgets = {
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

JobWorkFabricItemSizeFormSet = inlineformset_factory(
    JobWorkFabricItem,
    JobWorkFabricItemSize,
    form=JobWorkFabricItemSizeForm,
    extra=1,
    can_delete=True
)


class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['name', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
