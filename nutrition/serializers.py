from rest_framework import serializers
from nutrition.models import FoodItem, FoodIntake

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

class FoodIntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodIntake
        fields = '__all__'