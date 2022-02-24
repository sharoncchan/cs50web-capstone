from django.contrib import admin
from .models import User, Category, Post, Comment
from mptt.admin import MPTTModelAdmin

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment, MPTTModelAdmin)





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =['name','slug']
    prepopulated_fields = {'slug':('name',)}


