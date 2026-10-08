from datetime import date
from pathlib import Path
from uuid import UUID

import sqlite_utils

from backend.migrations import migrations
from backend.models import Exercise, Set, SetResult, Workout, WorkoutResult

DB_PATH = Path(__file__).parent / "database.db"


def get_db() -> sqlite_utils.Database:
    db = sqlite_utils.Database(DB_PATH)
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init_db() -> None:
    migrations.apply(get_db())


def get_workout_by_date(db: sqlite_utils.Database, workout_date: date) -> Workout | None:
    rows = list(db["workouts"].rows_where("workout_date = ?", [workout_date.isoformat()]))
    if not rows:
        return None
    row = rows[0]
    exercises = []
    for ex in db["exercises"].rows_where("workout_id = ?", [row["id"]], order_by="position"):
        sets = [
            Set(**{k: v for k, v in s.items() if k not in ("exercise_id", "position")})
            for s in db["sets"].rows_where("exercise_id = ?", [ex["id"]], order_by="position")
        ]
        exercises.append(Exercise(id=ex["id"], name=ex["name"], sets=sets))
    return Workout(
        id=row["id"],
        workout_date=row["workout_date"],
        exercises=exercises,
        suggested_calibration=row["suggested_calibration"],
    )


def save_workout(db: sqlite_utils.Database, workout: Workout) -> None:
    with db.conn:
        db["workouts"].insert({
            "id": str(workout.id),
            "workout_date": workout.workout_date.isoformat(),
            "suggested_calibration": workout.suggested_calibration,
        })
        for ex_pos, ex in enumerate(workout.exercises):
            db["exercises"].insert({
                "id": str(ex.id), "workout_id": str(workout.id),
                "name": ex.name, "position": ex_pos,
            })
            for set_pos, s in enumerate(ex.sets):
                db["sets"].insert({
                    "id": str(s.id), "exercise_id": str(ex.id), "kind": s.kind,
                    "position": set_pos, "n_reps": s.n_reps, "weight": s.weight,
                    "progressive_factor": s.progressive_factor,
                    "deload_factor": s.deload_factor,
                })


def list_results(db: sqlite_utils.Database) -> list[WorkoutResult]:
    results = []
    for r in db["workout_results"].rows:
        set_results = [
            SetResult(
                id=sr["id"], set_id=sr["set_id"], completed=bool(sr["completed"]),
                n_reps_completed=sr["n_reps_completed"],
                weight_completed=sr["weight_completed"], notes=sr["notes"],
            )
            for sr in db["set_results"].rows_where("workout_result_id = ?", [r["id"]])
        ]
        results.append(WorkoutResult(
            id=r["id"], workout_id=r["workout_id"],
            duration_seconds=r["duration_seconds"], notes=r["notes"],
            set_results=set_results,
        ))
    return results


def save_result(db: sqlite_utils.Database, result: WorkoutResult) -> None:
    with db.conn:
        db["workout_results"].insert({
            "id": str(result.id), "workout_id": str(result.workout_id),
            "duration_seconds": result.duration_seconds, "notes": result.notes,
        })
        for sr in result.set_results:
            db["set_results"].insert({
                "id": str(sr.id), "workout_result_id": str(result.id),
                "set_id": str(sr.set_id), "completed": int(sr.completed),
                "n_reps_completed": sr.n_reps_completed,
                "weight_completed": sr.weight_completed, "notes": sr.notes,
            })


def set_workout_calibration(db: sqlite_utils.Database, workout_id: UUID, calibration: float) -> None:
    with db.conn:
        db["workouts"].update(str(workout_id), {"suggested_calibration": calibration})
