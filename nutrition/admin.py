from django.contrib import admin
from nutrition.models import FoodItem, FoodIntake

# Register your models here.
class FoodIntakeAdmin(admin.ModelAdmin):
    list_display = ['user', 'food_item', 'date']

admin.site.register(FoodItem),
admin.site.register(FoodIntake, FoodIntakeAdmin),