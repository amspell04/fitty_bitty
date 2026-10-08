from sqlite_utils import Migrations

migrations = Migrations("fitty_bitty")


@migrations()
def create_workouts_table(db):
    db["workouts"].create(
        {"id": str, "workout_date": str, "suggested_calibration": float},
        pk="id",
        not_null={"workout_date"},
    )
    db["workouts"].create_index(["workout_date"], unique=True)


@migrations()
def create_exercises_table(db):
    db["exercises"].create(
        {"id": str, "workout_id": str, "name": str, "position": int},
        pk="id",
        not_null={"workout_id", "name", "position"},
        foreign_keys=[("workout_id", "workouts", "id")],
    )
    db["exercises"].create_index(["workout_id"])


@migrations()
def create_sets_table(db):
    db["sets"].create(
        {
            "id": str,
            "exercise_id": str,
            "kind": str,
            "position": int,
            "n_reps": int,
            "weight": float,
            "progressive_factor": float,
            "deload_factor": float,
        },
        pk="id",
        not_null={"exercise_id", "kind", "position", "n_reps", "weight"},
        foreign_keys=[("exercise_id", "exercises", "id")],
    )
    db["sets"].create_index(["exercise_id"])
    db.execute("CREATE TRIGGER sets_kind_check BEFORE INSERT ON sets "
               "WHEN NEW.kind NOT IN ('warmup', 'working') "
               "BEGIN SELECT RAISE(ABORT, 'kind must be warmup or working'); END")


@migrations()
def create_workout_results_table(db):
    db["workout_results"].create(
        {"id": str, "workout_id": str, "duration_seconds": float, "notes": str},
        pk="id",
        not_null={"workout_id"},
        foreign_keys=[("workout_id", "workouts", "id")],
    )
    db["workout_results"].create_index(["workout_id"], unique=True)


@migrations()
def create_set_results_table(db):
    db["set_results"].create(
        {
            "id": str,
            "workout_result_id": str,
            "set_id": str,
            "completed": int,
            "n_reps_completed": int,
            "weight_completed": float,
            "notes": str,
        },
        pk="id",
        not_null={"workout_result_id", "set_id", "completed"},
        defaults={"completed": 0},
        foreign_keys=[
            ("workout_result_id", "workout_results", "id"),
            ("set_id", "sets", "id"),
        ],
    )
    db["set_results"].create_index(["workout_result_id"])
    db["set_results"].create_index(["set_id"])
