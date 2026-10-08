from datetime import date
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Set(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    kind: Literal["warmup", "working"]
    n_reps: int
    weight: float
    progressive_factor: float | None = None
    deload_factor: float | None = None


class Exercise(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    sets: list[Set]


class Workout(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    workout_date: date
    exercises: list[Exercise]
    suggested_calibration: float | None = None


class SetResult(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    set_id: UUID
    completed: bool = False
    n_reps_completed: int | None = None
    weight_completed: float | None = None
    notes: str | None = None


class WorkoutResult(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    workout_id: UUID
    duration_seconds: float | None = None
    notes: str | None = None
    set_results: list[SetResult] = []


class FittyResponse(BaseModel):
    response: str
    session_id: str
