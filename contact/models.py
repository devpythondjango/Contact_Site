from django.db import models
from .validators import validate_passport_serial
from django.templatetags.static import static
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.


class HujumTuri(models.Model):
    hujum_name = models.CharField(max_length=50, null=True, blank=True)
    hujum_text = models.TextField(null=True)
    img = models.ImageField(upload_to='img/', null=True)

    def __str__(self):
        return self.hujum_name

    @property
    def get_img(self):
        return self.img.url if self.img else static('')


class Tuman(models.Model):
    tuman_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.tuman_name


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

    def save(self, *args, **kwargs):
        # Vaqt ma'lumotlarini o'zgartirish paytida timezone.now() ishlatish
        self.vaqt = timezone.now()
        super(Application, self).save(*args, **kwargs)

class ApplicationCreate(models.Model):
    application = models.OneToOneField(Application, related_name='app_create', on_delete=models.SET_NULL, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    createdate = models.DateTimeField(auto_now_add=True)
    body = models.TextField(null=True, blank=True)
    STATUS_CHOICES = (
        ('yangi', 'Yangi'),
        ('tekshirilmoqda', 'Tekshirilmoqda'),
        ('tekshirildi', 'Tekshirildi'),
        ('rad etildi', 'Rad etildi'),
        ('ma\'lumot topilmadi', 'Ma\'lumot topilmadi'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='yangi', null=True)

    class Meta:
        ordering = ['-update', '-createdate', '-id']

    def __str__(self):
        return self.application.first_name if self.application else 'Foydalanuvchi yuq'

@receiver(post_save, sender=Application)
def create_application_create(sender, instance, created, **kwargs):
    """
    Signal receiver to create or update ApplicationCreate when an Application is saved.
    """
    if created:
        # If a new Application is created, create a corresponding ApplicationCreate instance
        ApplicationCreate.objects.create(application=instance, body="")

    else:
        # If an existing Application is updated, update the corresponding ApplicationCreate instance
        application_create_instance = ApplicationCreate.objects.get(application=instance)
        application_create_instance.body = ""
        application_create_instance.save()