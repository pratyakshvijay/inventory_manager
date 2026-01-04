from django import forms
from .models import SKU
from django.forms import formset_factory

class ManualAdjustForm(forms.Form):
    sku = forms.ModelChoiceField(queryset=SKU.objects.all())
    quantity_change = forms.IntegerField()
    notes = forms.CharField(widget=forms.Textarea, required=False)

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Upload Excel File')

class OrderFileUploadForm(forms.Form):
    file = forms.FileField()

class SKUCreateForm(forms.Form):
    sku_code = forms.CharField(max_length=50)
    product_name = forms.CharField(max_length=255)
    stock_quantity = forms.IntegerField(min_value=0)

class SKUExcelUploadForm(forms.Form):
    file = forms.FileField()

class BagForm(forms.Form):
    bag_number = forms.CharField(label='Bag Number', max_length=50)
    reflect_in_rack = forms.BooleanField(
        label='Add to Rack (do not affect master stock)',
        required=False
    )

class BagItemForm(forms.Form):
    sku = forms.ModelChoiceField(
        queryset=SKU.objects.none(),  # Initially none for AJAX
        widget=forms.Select(attrs={'class': 'form-control sku-dropdown'})
    )
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter quantity'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ Ensure proper queryset for form validation and rendering
        self.fields['sku'].queryset = SKU.objects.all()

# Formset definition
BagItemFormSet = formset_factory(BagItemForm, extra=1)
