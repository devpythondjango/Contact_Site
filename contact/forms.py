from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "surname": forms.TextInput(attrs={'class': 'form-control'}),
            "birthday": forms.DateInput(attrs={'class': 'form-control'}),
            "passport_serial": forms.TextInput(attrs={'class': 'form-control'}),    
            "phone": forms.TextInput(attrs={'class': 'form-control'}),
            "address": forms.TextInput(attrs={'class': 'form-control'}),
            "gender": forms.Select(attrs={'class': 'form-control bg-transparent border-primary p-3'}),
            "district": forms.Select(attrs={'class': 'form-control bg-transparent border-primary p-3', 'required': True}),
            "text": forms.TextInput(attrs={'class': 'form-control'}),
            "hujumturi": forms.Select(attrs={'class': 'form-control bg-transparent border-primary p-3 bi bi-arrow-right', 'id': 'id_hujumturi', 'onchange': 'showDiv(this)', 'required': True}),
            "plastikraqam_ozi": forms.NumberInput(attrs={'class': 'form-control'}),
            "plastikraqam_gumondor": forms.NumberInput(attrs={'class': 'form-control'}),
            "full_name_gumondor": forms.TextInput(attrs={'class': 'form-control'}),
            "phone_gumondor": forms.TextInput(attrs={'class': 'form-control'}),
            "sana": forms.DateInput(attrs={'class': 'form-control'}),
            "vaqt": forms.DateTimeInput(attrs={'class': 'form-control'}),
            "summa": forms.NumberInput(attrs={'class': 'form-control'}),
            "rasm": forms.FileInput(attrs={'class': 'form-control'}),
            "ilova": forms.TextInput(attrs={'class': 'form-control'}),
            "ilova_gumondor": forms.TextInput(attrs={'class': 'form-control'}),
        }

