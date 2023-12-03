from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="media/profiles/", null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_avatar(self):
        return self.avatar.url if self.avatar else static("dashboard/dist/img/user2-160x160.jpg")