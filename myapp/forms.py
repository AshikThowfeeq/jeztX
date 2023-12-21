from django import forms
from .models import ServerInfo, PersonData

class CameraAssignmentForm(forms.Form):
    camera = forms.ModelChoiceField(
        queryset=ServerInfo.objects.all(), 
        empty_label="Select Camera",
        widget=forms.Select(attrs={'class': 'color-picker asColorPicker-input'})
    )
    employee_id = forms.CharField(
        label="Employee ID",
        widget=forms.TextInput(attrs={
            'class': 'color-picker asColorPicker-input',
            'placeholder': 'Employee Id'  # Adding placeholder here
        })  # Adding placeholder here)
    )