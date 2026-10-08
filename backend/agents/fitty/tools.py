from backend.models import Workout, WorkoutResult



def apply_calibration(rating: int, todays_workout: Workout) -> str:
    '''Calibrates the users given workout based on how they are feeling today.'''

    if rating <= 3:
        todays_workout.suggested_calibration = .3
    if rating > 3 and rating < 5:
        todays_workout.suggested_calibration = .2
    if rating >= 5 and rating < 8:
        todays_workout.suggested_calibration = .1
    if rating >= 8:
        todays_workout.suggested_calibration = 1.1

    return f"Calibration successful. Suggested calibration set to {todays_workout.suggested_calibration} for today's workout."

