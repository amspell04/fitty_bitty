from backend.models import Workout, WorkoutResult
import sqlite3

def make_db_connection():
    conn = sqlite3.connect("database.db")
    return conn.cursor()


def get_todays_workout(date: str, ):
    cursor = make_db_connection()
    cursor.execute("SELECT * from workout_program where  ")
    
    # return todays workout
    return Workout

def post_result():

    # post todays result
    return WorkoutResult
