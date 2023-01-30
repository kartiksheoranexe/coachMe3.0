from rest_framework import serializers
from panalyzer.models import TrainingSplit, MuscleParts, ExerciseSelection, LogPerformance, HeartPerformance, WeeklyCheckins, Picture


class TrainingSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingSplit
        fields = ['id', 'coach', 'client', 'pre_def',
                  'split_name', 'split_desc', 'split_days']


class ExerciseSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSelection
        fields = ['id', 'muscle', 'exercise_name',
                  'sets', 'rep_range', 'exercise_description']


class MusclePartsSerializer(serializers.ModelSerializer):
    exercise_selections = ExerciseSelectionSerializer(many=True)

    class Meta:
        model = MuscleParts
        fields = ['id', 'split', 'muscles',
                  'total_sets', 'exercise_selections']

class MusclePartsExcelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MuscleParts
        fields = ['id', 'split', 'muscles',
                  'total_sets']

class LogPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogPerformance
        fields = [
            'id',
            'client',
            'training_day',
            'exercise',
            'workout_num',
            'set_num',
            'weight_unit',
            'weight',
            'reps',
        ]

class HeartPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeartPerformance
        fields = ['resting_heart_rate', 'maximum_heart_rate', 'timestamp']

class HeartPerformanceMinMaxSerializer(serializers.Serializer):
    min = serializers.IntegerField()
    max = serializers.IntegerField()

class WeeklyCheckinsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WeeklyCheckins
        fields = [
            'starting_weight',
            'current_weight',
            'energy_levels',
            'strength_levels',
            'waist',
            'hips',
            'right_arm',
            'right_quad',
            'right_calf',
        ]