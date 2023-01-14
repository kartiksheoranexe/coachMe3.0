from django.urls import path

from . import views
from panalyzer.views import CreateWorkoutPlan, LogPerformanceCreateView, CalculateMuscleLoadView, HeartPerformanceView

urlpatterns = [
    path('create-workout-plan/', CreateWorkoutPlan.as_view(), name='register'),
    path('log-performance/', LogPerformanceCreateView.as_view(), name='log-performance-create'),
    path('calculate-muscle-load/', CalculateMuscleLoadView.as_view(), name='performance-muscle-load'),
    path('heart-performance/', HeartPerformanceView.as_view(), name='heart-performance'),
]
