from .models import Customer, Vehicle, Visit, RepairJob
from .models import Vehicle
from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control'
            })
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['number_plate', 'vehicle_type', 'customer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['number_plate'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['vehicle_type'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Vehicle Type'
        })

        self.fields['customer'].widget.attrs.update({
            'class': 'form-select selectpicker',
            'data-live-search': 'true'
        })

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['vehicle', 'notes', 'km_reading']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['vehicle'].widget.attrs.update({
            'class': 'form-select selectpicker',
            'data-live-search': 'true'
        })

        self.fields['km_reading'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['notes'].widget.attrs.update({
            'class': 'form-control'
        })

class RepairJobForm(forms.ModelForm):
    class Meta:
        model = RepairJob
        fields = '__all__'

