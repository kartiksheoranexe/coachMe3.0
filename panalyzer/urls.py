from django.urls import path

from . import views
from panalyzer.views import CreateWorkoutPlan, LogPerformanceCreateView, CalculateMuscleLoadView, HeartPerformanceView, ExcelTrainingDesignView, ExcelExerciseSelectionView, ExcelWorkoutCreationView

urlpatterns = [
    path('create-workout-plan/', CreateWorkoutPlan.as_view(), name='register'),
    path('log-performance/', LogPerformanceCreateView.as_view(), name='log-performance-create'),
    path('calculate-muscle-load/', CalculateMuscleLoadView.as_view(), name='performance-muscle-load'),
    path('heart-performance/', HeartPerformanceView.as_view(), name='heart-performance'),

    #api to parse 
    path('design-training-excel/', ExcelTrainingDesignView.as_view(), name='design-training-excel'),
    path('exercise-selection-excel/', ExcelExerciseSelectionView.as_view(), name='exercise-selection-excel'),
    path('workout-creation-excel/', ExcelWorkoutCreationView.as_view(), name='workout-creation-excel'),
]
