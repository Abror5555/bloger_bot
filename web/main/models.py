from django.db import models

# Create your models here.

SOCIAL_MEDIA_CHOICES = (
    ("instagram", "Instagarm"),
    ("tik tok", "Tik Tok"),
    ("telegram", "Instagarm"),
)


class Bloger(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="users", blank=True, null=True, unique=True)

    def __str__(self):
        return  self.name


class User(models.Model):
    id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    social_media = models.CharField(choices=SOCIAL_MEDIA_CHOICES, max_length=10, blank=True, null=True)

    bloger = models.ForeignKey(Bloger, on_delete=models.CASCADE, null=True, blank=True, related_name="bloger")
    
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name



