from django.db import models
from main.models import CustomUser

# Create your models here.
SERVING_TYPE_CHOICES = (
    ('ounce', 'Ounce'),
    ('gram', 'Gram'),
    ('pound', 'Pound'),
    ('kilogram', 'Kilogram'),
    ('pinch', 'Pinch'),
    ('liter', 'Liter'),
    ('fluid ounce', 'Fluid ounce'),
    ('gallon', 'Gallon'),
    ('pint', 'Pint'),
    ('quart', 'Quart'),
    ('milliliter', 'Milliliter'),
    ('drop', 'Drop'),
    ('cup', 'Cup'),
    ('tablespoon', 'Tablespoon'),
    ('teaspoon', 'Teaspoon'),
)

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    serving_size = models.FloatField(default=0)
    serving_type = models.CharField(max_length=20, choices=SERVING_TYPE_CHOICES)
    sugar_ad = models.FloatField(default=0)
    calcium = models.FloatField(default=0)
    carbs_net = models.FloatField(default=0)
    carbs_diff = models.FloatField(default=0)
    cholestrol = models.FloatField(default=0)
    calories = models.FloatField(default=0)
    fa_monounsaturated = models.FloatField(default=0)
    fa_polyunsaturated = models.FloatField(default=0)
    fa_totalsaturated = models.FloatField(default=0)
    fa_totaltrans = models.FloatField(default=0)
    fibre = models.FloatField(default=0)
    dfe_folate = models.FloatField(default=0)
    folate_food = models.FloatField(default=0)
    folic_acid = models.FloatField(default=0)
    iron = models.FloatField(default=0)
    magnesium = models.FloatField(default=0)
    niacin = models.FloatField(default=0)
    phosphorus = models.FloatField(default=0)
    potassium = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    riboflavin = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    sugar_alcohal = models.FloatField(default=0)
    sugar_total = models.FloatField(default=0)
    thiamin = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    vitamin_a = models.FloatField(default=0)
    vitamin_b12 = models.FloatField(default=0)
    vitamin_b6 = models.FloatField(default=0)
    vitamin_c = models.FloatField(default=0)
    vitamin_d = models.FloatField(default=0)
    vitamin_e = models.FloatField(default=0)
    vitamin_k = models.FloatField(default=0)
    water = models.FloatField(default=0)
    zinc = models.FloatField(default=0)

    def __str__(self):
        return self.name

class FoodIntake(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
        