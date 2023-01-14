from panalyzer.models import LogPerformance


def calculate_muscle_load(client_id):
    muscle_load_by_workout = {}
    log_entries = LogPerformance.objects.filter(client_id=client_id)

    for entry in log_entries:
        muscle_load = entry.weight * entry.reps
        if entry.workout_num in muscle_load_by_workout:
            if entry.exercise.exercise_name in muscle_load_by_workout[entry.workout_num]:
                muscle_load_by_workout[entry.workout_num][entry.exercise.exercise_name] += muscle_load
            else:
                muscle_load_by_workout[entry.workout_num][entry.exercise.exercise_name] = muscle_load
        else:
            muscle_load_by_workout[entry.workout_num] = {
                entry.exercise.exercise_name: muscle_load
            }

    for workout_num in muscle_load_by_workout:
        total_muscle_load = sum(muscle_load_by_workout[workout_num].values())
        muscle_load_by_workout[workout_num]["Total_Muscle_Load"] = total_muscle_load

    return muscle_load_by_workout
