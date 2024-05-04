from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Recipe, CustomUser, Comment
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    """This class is for categories in the admin panel"""

    list_display = ("pk", "name", "created", "updated", "published")
    list_display_links = ("pk", "name")
    list_editable = ("published", )
    list_filter = ("published", )


class RecipeAdmin(admin.ModelAdmin):
    """This class is for recipes in the admin panel"""

    list_display = ("pk", "name", "views_count", "author", "category", "created",
                    "updated", "published", "get_photo")
    list_display_links = ("pk", "name")
    list_editable = ("category", "published")
    list_filter = ("published", "category")
    search_fields = ("name", "content")

    def get_photo(self, recipe):
        """get the picture"""

        if recipe.photo:
            img_url = recipe.photo.url
        else:
            img_url = "https://bitsofco.de/img/Qo5mfYDE5v-350.png"
        return mark_safe(f'<img src="{img_url}" width="75px">')
    get_photo.short_description = "Photo"


class CommentAdmin(admin.ModelAdmin):
    """For comments in the admin panel"""

    list_display = ('pk', 'commentator', 'text', 'created', 'post_id')
    list_display_links = ('pk', 'commentator')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(CustomUser)
admin.site.register(Comment, CommentAdmin)
