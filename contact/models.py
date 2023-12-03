from django.db import models
from .validators import validate_passport_serial
from django.templatetags.static import static

# Create your models here.


class HujumTuri(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Tuman(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_CHOICES = (
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol'),
    )
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    passport_serial = models.CharField(max_length=9, validators=[validate_passport_serial], null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=5, choices=STATUS_CHOICES, null=True)
    district = models.ForeignKey(Tuman, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    hujumturi = models.ForeignKey(HujumTuri, on_delete=models.SET_NULL, null=True, blank=True)
    plastikraqam_ozi = models.IntegerField(null=True, blank=True)
    plastikraqam_gumondor = models.IntegerField(null=True, blank=True)
    full_name_gumondor = models.CharField(max_length=255, null=True, blank=True)
    phone_gumondor = models.CharField(max_length=32, null=True, blank=True)
    sana = models.DateField(null=True, blank=True)
    vaqt = models.DateTimeField(null=True, blank=True)
    summa = models.IntegerField(null=True, blank=True)
    rasm = models.ImageField(upload_to='chek_rasm/', null=True, blank=True)
    ilova = models.CharField(max_length=50, null=True, blank=True)
    ilova_gumondor = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_image(self):
        return self.rasm.url if self.rasm else static('')

class ApplicationCreate(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    createdate = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=True, blank=True)
    STATUS_CHOICES = (
        ('yangi', 'Yangi'),
        ('tekshirilmoqda', 'Tekshirilmoqda'),

        ('tekshirilmoqda', 'Tekshirilmoqda'),
        ('rad etildi', 'Rad etildi'),
        ('tekshirildi', 'Tekshirildi'),
    )
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='yangi', null=True)

    class Meta:
        ordering = ['-update', '-createdate']

    def __str__(self):
        return self.application.first_name if self.application else 'Foydalanuvchi yuq'
