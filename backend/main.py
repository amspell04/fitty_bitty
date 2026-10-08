import sqlite3
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException
from google.adk.cli.fast_api import get_fast_api_app

from backend import db as store
from backend.mcp_server import mcp
from backend.models import Workout, WorkoutResult

BASE_DIR = Path(__file__).parent
AGENTS_DIR = str(BASE_DIR / "agents")
PREFIX = "/fitty-bitty"


@asynccontextmanager
async def lifespan(_: FastAPI):
    store.init_db()
    async with mcp.session_manager.run():
        yield


app = get_fast_api_app(
    agents_dir=AGENTS_DIR,
    session_service_uri=f"sqlite:///{BASE_DIR / 'sessions.db'}",
    allow_origins=["*"],
    web=False,
    lifespan=lifespan,
)


app.mount("/mcp", mcp.streamable_http_app())


@app.get(f"{PREFIX}/today")
def get_todays_workout() -> Workout:
    workout = store.get_workout_by_date(store.get_db(), date.today())
    if workout is None:
        raise HTTPException(status_code=404, detail="No workout scheduled for today")
    return workout


@app.get(f"{PREFIX}/results")
def get_results() -> list[WorkoutResult]:
    return store.list_results(store.get_db())


@app.post(f"{PREFIX}/results", status_code=201)
def post_result(result: WorkoutResult) -> WorkoutResult:
    try:
        store.save_result(store.get_db(), result)
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return result
