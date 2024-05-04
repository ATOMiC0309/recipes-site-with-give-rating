from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpRequest

from .models import Category, Recipe, CustomUser, Comment, Rating
from .forms import RecipeForm, CategoryForm, LoginForm, RegisterForm, CommentForm



# Create your views here.


def index(request):
    """Home page"""

    recipes = Recipe.objects.all()
    context = {
        "recipes": recipes
    }

    return render(request, 'app/index.html', context=context)


@permission_required('app.view_recipe', login_url='login')
def all_recipes_by_category(request, category):
    """for View recipes by category"""

    category = Category.objects.get(name=category)
    recipes = Recipe.objects.filter(category=category)

    context = {
        "recipes": recipes
    }

    return render(request, 'app/index.html', context=context)


@permission_required('app.view_recipe', login_url='login')
def recipe_detail(request, pk):
    """for Recipe view detail"""

    comments = Comment.objects.filter(post_id=pk)
    recipe = Recipe.objects.get(pk=pk)
    recipe.views_count += 1
    recipe.save()
    context = {
        "recipe": recipe,
        'form': CommentForm(),
        'comments': comments
    }
    rating = Rating.objects.filter(post=recipe, user=request.user.id).first()
    recipe.user_rating = rating.rating if rating else 0
    return render(request, 'app/recipe_detail.html', context=context)


@permission_required('app.add_recipe', login_url='page404')
def recipe_create(request):
    """for Recipe create """

    recipe_form = RecipeForm(data=request.POST, files=request.FILES)
    if recipe_form.is_valid():
        recipe = recipe_form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        messages.success(request, "Content created successfully!")
        return redirect('index')

    recipe_form = RecipeForm()
    context = {
        'recipe_form': recipe_form,
    }
    return render(request, 'app/recipe_form.html', context=context)


@permission_required('app.change_recipe', login_url='page404')
def recipe_update(request, pk):
    """for  Recipe update(change)"""

    recipe = Recipe.objects.get(pk=pk)

    recipe_form = RecipeForm(data=request.POST or None, instance=recipe, files=request.FILES or None)
    if recipe_form.is_valid():
        recipe_form.save()
        messages.info(request, "Content edited successfully!")
        return redirect('index')

    context = {
        'recipe_form': recipe_form,
    }
    return render(request, 'app/recipe_form.html', context=context)


@permission_required('app.delete_recipe', login_url='page404')
def recipe_delete(request, pk):
    """for recipe delete"""

    recipe = Recipe.objects.get(pk=pk)

    if request.method == 'POST':
        recipe.delete()
        messages.warning(request, "You have deleted the post!")
        return redirect('index')

    return render(request, 'app/recipe_delete.html', {"recipe": recipe})


@permission_required('app.view_category', login_url='login')
def all_categories(request):
    """get all category"""

    categories = Category.objects.all()
    return render(request, 'app/categories.html', context={"categories": categories})


@permission_required('app.add_category', login_url='page404')
def category_create(request):
    """for category create"""

    category_form = CategoryForm(data=request.POST)
    if category_form.is_valid():
        category_form.save()
        messages.success(request, "Category created successfully!")
        return redirect('all_categories')

    category_form = CategoryForm()
    context = {
        'category_form': category_form,
    }
    return render(request, 'app/category_form.html', context=context)


@permission_required('app.change_category', login_url='page404')
def category_update(request, pk):
    """for category update"""

    category = Category.objects.get(pk=pk)

    category_form = CategoryForm(data=request.POST or None, instance=category)
    if category_form.is_valid():
        category_form.save()
        messages.info(request, "Category edited successfully!")
        return redirect('all_categories')

    context = {
        'category_form': category_form,
    }
    return render(request, 'app/category_form.html', context=context)


@permission_required('app.delete_category', login_url='page404')
def category_delete(request, pk):
    """for category update"""

    category = Category.objects.get(pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.warning(request, "You have deleted the category!")
        return redirect('all_categories')

    return render(request, 'app/category_delete.html', {"category": category})


def user_login(request):
    """This is for login"""

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'{user.username.title()}, you have successfully entered the site.')
            return redirect('index')

        if form.errors:
            messages.error(request, "Check that the fields are correct!")

    form = LoginForm()
    context = {
        'form': form,
        'title': 'Sign in'
    }
    return render(request, 'app/login.html', context=context)


def user_logout(request):
    """This is for logout"""

    logout(request)
    messages.warning(request, "You are logged out!")
    return redirect('login')


def user_register(request):
    """This is for sing up"""

    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "You can log in by entering your username and password.")
            return redirect('login')

        if form.errors:
            messages.error(request, "Check that the fields are correct!")

    form = RegisterForm()
    context = {
        'form': form,
        'title': 'Sign up'
    }
    return render(request, 'app/register.html', context=context)


def profile(request, username):
    """This is for user profil"""

    if request.user.username == username or request.user.is_superuser:
        user = User.objects.get(username=username)
        recipes = Recipe.objects.filter(author=user)
        context = {
            'user': user,
            'recipes': recipes
        }
        try:
            custom_user = CustomUser.objects.get(user=user)
            context['custom_user'] = custom_user
        except:
            pass
        return render(request, 'app/profile.html', context=context)

    return redirect('page404')


def page_not_found(request):
    """This is for page not found"""

    messages.warning(request, "It's page not found!")
    return render(request, 'app/page_not_found.html')


def save_comment(request, pk):
    if request.method == 'POST':
        recipe = Recipe.objects.get(pk=pk)
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = recipe
            comment.commentator = request.user
            comment.save()
            messages.success(request, f'Comment successfully added the site.')
            return redirect('recipe_detail', pk=pk)

    return redirect('page404')


def rate(request: HttpRequest, post_id: int, rating: int) -> HttpResponse:
    post = Recipe.objects.get(id=post_id)
    Rating.objects.filter(post=post, user=request.user).delete()
    post.rating_set.create(user=request.user, rating=rating)
    return recipe_detail(request, post_id)
