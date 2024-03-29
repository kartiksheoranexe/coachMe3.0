from django.contrib import admin
from panalyzer.models import TrainingSplit, MuscleParts, ExerciseSelection, LogPerformance, HeartPerformance, WeeklyCheckins, Picture

# Register your models here.


class TrainingSplitAdmin(admin.ModelAdmin):
    list_display = ['coach', 'client', 'split_name']


class MusclePartAdmin(admin.ModelAdmin):
    list_display = ['split', 'muscles']

class LogPerformanceAdmin(admin.ModelAdmin):
    list_display = ['client', 'exercise', 'workout_num']

class HeartPerformanceAdmin(admin.ModelAdmin):
    list_display = ['client', 'resting_heart_rate', 'maximum_heart_rate', 'timestamp']

class WeeklyCheckinsAdmin(admin.ModelAdmin):
    list_display = ['coach', 'client', 'created_at']

admin.site.register(TrainingSplit, TrainingSplitAdmin),
admin.site.register(MuscleParts, MusclePartAdmin),
admin.site.register(ExerciseSelection),
admin.site.register(LogPerformance, LogPerformanceAdmin),
admin.site.register(HeartPerformance, HeartPerformanceAdmin),
admin.site.register(WeeklyCheckins, WeeklyCheckinsAdmin),
admin.site.register(Picture)

