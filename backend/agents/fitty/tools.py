from backend.models import Workout, WorkoutResult



def calibrate_workout(rating: int, todays_workout: Workout) -> str:
    '''Calibrates the users given workout based on how they are feeling today.'''

    calibration_factor: float = 0.0

    if rating <= 3:
        calibration_factor = .3
    if rating > 3 and rating < 5:
        calibration_factor = .2
    if rating >= 5 and rating < 8:
        calibration_factor = .1
    if rating >= 8:
        calibration_factor = 1.1

    for set in todays_workout.sets:
        for rep in set.working:
            rep.suggested_calibration = calibration_factor

    return f"Calibration successful. Suggested calibration set to {calibration_factor} for today's workout."


def e1rm(weight, reps, rpe):
    effective_reps = reps + (10 - rpe)
    return weight * (1 + effective_reps / 30)

def next_weight(weight, reported_rpe, target_rpe=8):
    diff = target_rpe - reported_rpe
    if diff >= 1:  return weight + 10
    if diff == 0:  return weight + 5
    if diff == -1: return weight
    return round(weight * 0.95 / 5) * 5  # round to nearest 5 lb