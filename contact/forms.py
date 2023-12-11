from django import forms
from .models import Application, Tuman, HujumTuri
from .validators import validate_passport_serial
from captcha.fields import CaptchaField

class SMSVerificationForm(forms.Form):
    sms_code = forms.CharField(
        max_length=6, 
        min_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': "id_smsCode"}))
    captcha = CaptchaField(required=False)
 

class ApplicationForm(forms.Form):
    STATUS_CHOICES = (
        ('jins', 'Jins'),
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol'),
    )

    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    surname = forms.CharField(max_length=50, required=False)
    birthday = forms.DateField(required=False)
    passport_serial = forms.CharField(max_length=9, validators=[validate_passport_serial], required=False)
    phone = forms.CharField(max_length=32, required=False)
    address = forms.CharField(max_length=255, required=False)
    gender = forms.ChoiceField(
        choices=STATUS_CHOICES, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control bg-transparent border-primary p-3'})
        )
    district = forms.ModelChoiceField(
        queryset=Tuman.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control bg-transparent border-primary p-3'})
    )
    text = forms.CharField(widget=forms.Textarea, required=False)

    hujumturi = forms.ModelChoiceField(
        queryset=HujumTuri.objects.all(), 
        required=False,
        widget=forms.Select(attrs={'class': 'form-control bg-transparent border-primary p-3','id': 'id_hujumturi', 'onchange': 'showDiv(this)',})
        )
    plastikraqam_ozi = forms.IntegerField(required=False)
    plastikraqam_gumondor = forms.IntegerField(required=False)
    full_name_gumondor = forms.CharField(max_length=255, required=False)
    phone_gumondor = forms.CharField(max_length=32, required=False)
    vaqt = forms.DateTimeField(required=False)
    summa = forms.IntegerField(required=False)
    rasm = forms.ImageField(required=False)
    ilova = forms.CharField(max_length=50, required=False)
    ilova_gumondor = forms.CharField(max_length=50, required=False)