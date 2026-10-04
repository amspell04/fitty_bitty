from typing import Optional

class Rep:
    n_reps: int
    weight: float
    progressive_factor: Optional[float]
    deload_factor: Optional[float]
    suggested_calibration: Optional[float]

class RepResult:
    n_reps_completed: int
    weight_completed: float

class Set:
    name: str
    warmup: list[Rep]
    working: list[Rep]

class SetResult:
    completed_set: bool
    notes: Optional[str]
    rep_result: list[RepResult]

class Workout:
    time_lenght: float
    sets: list[Set]

class WorkoutResult:
    time_length: float
    sets_results: list[SetResult]


