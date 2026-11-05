from django import forms
from .models import RubbishDetail


class RubbishDetailForm(forms.ModelForm):
    class Meta:
        model = RubbishDetail
        fields = ['category', 'name', 'rate', 'unit', 'weight',
                  'description', 'is_hazardous', 'is_recyclable', 'is_active']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = 'form-check-input'
            elif isinstance(widget, forms.Select):
                widget.attrs['class'] = 'form-select'
            else:
                widget.attrs['class'] = 'form-control'
