from datetime import date

from mcp.server.fastmcp import FastMCP

from backend import db as store
from backend.agents.fitty.tools import apply_calibration
from backend.models import Workout

mcp = FastMCP("fitty-bitty", streamable_http_path="/", stateless_http=True)


@mcp.tool()
def get_workout() -> Workout | None:
    """Get the user's workout scheduled for today, or null if none is scheduled."""
    return store.get_workout_by_date(store.get_db(), date.today())


@mcp.tool()
def calibrate_workout(rating: int) -> str:
    """Calibrate today's workout based on how the user feels, on a scale of 1 (awful) to 10 (great)."""
    if not 1 <= rating <= 10:
        return "Rating must be between 1 and 10."
    db = store.get_db()
    workout = store.get_workout_by_date(db, date.today())
    if workout is None:
        return "No workout is scheduled for today."
    message = apply_calibration(rating, workout)
    store.set_workout_calibration(db, workout.id, workout.suggested_calibration)
    return message
