from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext
from django.templatetags.static import static
# Create your models here.

class Profile(models.Model): 
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profiles/", null=True, blank=True)
    bg_avatar = models.ImageField(upload_to="profiles/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = gettext('Profile')
        verbose_name_plural = gettext('Profiles')

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static("images/logo/default-profile-picture.png")

    @property
    def get_bg_avatar(self):
        return self.bg_avatar.url if self.bg_avatar else static("images/logo/profile_bg.jpg")