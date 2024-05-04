from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (index, all_recipes_by_category, recipe_detail, recipe_create, recipe_update, recipe_delete,
                    all_categories, category_create, category_update, category_delete, user_login, user_logout,
                    user_register, page_not_found, profile, save_comment, rate)
urlpatterns = [
    path('', index, name="index"),
    path('category/<str:category>/', all_recipes_by_category, name="recipes_by_category"),
    path('recipe-detail/<int:pk>/', recipe_detail, name="recipe_detail"),
    path('recipe-create/', recipe_create, name="recipe_create"),
    path('recipe-update/<int:pk>/', recipe_update, name="recipe_update"),
    path('recipe-delete/<int:pk>/', recipe_delete, name="recipe_delete"),
    path('all-category/', all_categories, name="all_categories"),
    path('category-create/', category_create, name="category_create"),
    path('category-update/<int:pk>/', category_update, name="category_update"),
    path('category-delete/<int:pk>/', category_delete, name="category_delete"),

    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('register/', user_register, name="register"),
    path('profile/<str:username>/', profile, name="profile"),

    path('page404/', page_not_found, name="page404"),
    path('save-comment/<int:pk>', save_comment, name="save_comment"),
    path('rate/<int:post_id>/<int:rating>/', rate),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
