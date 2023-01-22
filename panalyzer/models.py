from django.db import models
from main.models import CustomUser, Coach, Client
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
SPLIT_TYPE = (
    ('FB', 'Full Body'),
    ('UL', 'Upper Lower'),
    ('PPL', 'Push, Pull, Legs'),
    ('BS', 'Bro Split'),
    ('CUS', 'Custom'),
)

MUSCLE_TYPE = (
    ('CH', 'Chest'),
    ('BA', 'Back'),
    ('LE', 'Legs'),
    ('SH', 'Shoulders'),
    ('AR', 'Arms'),
    ('AB', 'Abs'),
)

WEIGHT_UNIT = (
    ('KG', 'kg'),
    ('LBS', 'lbs'),
)


class TrainingSplit(models.Model):
    coach = models.ForeignKey(
        Coach, on_delete=models.CASCADE, default=None, related_name='Coach')
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, default=None, related_name='Client')
    pre_def = models.CharField(max_length=3, choices=SPLIT_TYPE)
    split_name = models.CharField(max_length=100)
    split_desc = models.TextField()
    split_days = models.CharField(max_length=100)

    def __str__(self):
        return self.split_name + ' - ' + self.coach.user.username


class MuscleParts(models.Model):
    split = models.ForeignKey(TrainingSplit, on_delete=models.CASCADE)
    muscles = models.CharField(max_length=2, choices=MUSCLE_TYPE)
    total_sets = models.IntegerField(null=True)

    def __str__(self):
        return self.muscles + " - " + self.split.split_name


class ExerciseSelection(models.Model):
    muscle = models.ForeignKey(MuscleParts, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    sets = models.IntegerField(null=True)
    rep_range = models.CharField(max_length=100, default=None, null=True)
    exercise_description = models.TextField(null=True)

    def __str__(self):
        return self.muscle.muscles + ' - ' + self.muscle.split.split_name + ' - ' + self.exercise_name


class LogPerformance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=None)
    training_day = models.CharField(max_length=50, default=None)
    exercise = models.ForeignKey(ExerciseSelection, on_delete=models.CASCADE)
    workout_num = models.IntegerField()
    set_num = models.IntegerField()
    weight_unit = models.CharField(max_length=3, choices=WEIGHT_UNIT)
    weight = models.IntegerField()
    reps = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )


class HeartPerformance(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    resting_heart_rate = models.IntegerField()
    maximum_heart_rate = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    