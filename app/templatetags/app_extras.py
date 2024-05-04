from django import template
from app.models import Category

register = template.Library()


@register.simple_tag
def all_categories():
    return Category.objects.all()
