from django.contrib import admin
from .models import User, Bloger
# Register your models here.





@admin.register(Bloger)
class BlogerAdmin(admin.ModelAdmin):
    model = Bloger
    list_display = ["name", "created", "user"]
    search_fields = ["name"]
    list_filter = ['created']
    

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ["id", "name", "phone_number", "bloger", "created", "social_media"]
    search_fields = ["name", "id", "phone_number", "social_media"]
    list_filter = ['created', "bloger", "social_media"]