from django.urls import path
from .views import get_csrf_token, FoodInfoView, AutoComplete, NutritionInformation, FoodIntakeListCreateAPIView, DeleteFoodIntakeObj, FoodIntakeDayView

urlpatterns = [
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('food-info/', FoodInfoView.as_view(), name='food-information'),
    path('auto-food-info/', AutoComplete.as_view(), name='auto-food-information'),
    path('nutrition-info/', NutritionInformation.as_view(), name='nutrition-information'),
    path('foodintakes/', FoodIntakeListCreateAPIView.as_view(), name='foodintake-list'),
    path('delete-foodintakes/', DeleteFoodIntakeObj.as_view(), name='delete-foodintake-obj'),
    path('day-foodintakes/', FoodIntakeDayView.as_view(), name='day-foodintake'),

]
