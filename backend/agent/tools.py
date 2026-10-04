from backend.models import Workout

def calibrate_workout(rating: int, todays_workout: Workout) -> str:
    '''Calibrates the users given workout based on how they are feeling today.'''

    calibration_factor: float = 0.0

    if rating <= 3:
        calibration_factor = .3
    if rating > 3 and rating < 5:
        calibration_factor = .2
    if rating >= 5 and rating < 8:
        calibration_factor = .1
    else:
        calibration_factor = 1.1

    for set in todays_workout.sets:
        for rep in set.working:
            rep.suggested_calibration = calibration_factor

    return f"Calibration successful. Suggested calibration set to {calibration_factor} for today's workout."