import os
import sqlite3
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session, flash
import joblib

from utils.advisory import (
    build_explanation,
    fertilizer_recommendation,
    pest_disease_advisory,
)
from utils.weather import get_weather

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "crop_advisory.db"
MODEL_PATH = BASE_DIR / "ml" / "model.pkl"


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

    initialize_database()

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"].strip()
            password = request.form["password"].strip()
            role = request.form.get("role", "farmer")
            if not username or not password:
                flash("Username and password are required.", "danger")
                return redirect(url_for("register"))

            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        (username, password, role),
                    )
                    conn.commit()
                except sqlite3.IntegrityError:
                    flash("Username already exists.", "warning")
                    return redirect(url_for("register"))

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"].strip()
            password = request.form["password"].strip()
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, role FROM users WHERE username = ? AND password = ?",
                    (username, password),
                )
                user = cursor.fetchone()
            if user:
                session["user_id"] = user[0]
                session["role"] = user[1]
                flash("Login successful.", "success")
                return redirect(url_for("dashboard"))
            flash("Invalid credentials.", "danger")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logged out successfully.", "info")
        return redirect(url_for("index"))

    def login_required(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("login"))
            return view_func(*args, **kwargs)

        return wrapper

    @app.route("/dashboard")
    @login_required
    def dashboard():
        latest = get_latest_advisory(session["user_id"])
        return render_template("dashboard.html", latest=latest)

    @app.route("/advisory", methods=["GET", "POST"])
    @login_required
    def advisory():
        if request.method == "POST":
            form_data = {
                "location": request.form["location"].strip(),
                "soil_ph": float(request.form["soil_ph"]),
                "nitrogen": float(request.form["nitrogen"]),
                "phosphorus": float(request.form["phosphorus"]),
                "potassium": float(request.form["potassium"]),
                "season": request.form["season"],
            }
            weather = get_weather(request.form["location"].strip())
            try:
                crop = predict_crop(
                    form_data["nitrogen"],
                    form_data["phosphorus"],
                    form_data["potassium"],
                    form_data["soil_ph"],
                    weather["rainfall"],
                    weather["temperature"],
                    weather["humidity"],
                )
            except FileNotFoundError as error:
                flash(str(error), "warning")
                return redirect(url_for("advisory"))
            fertilizer = fertilizer_recommendation(
                form_data["nitrogen"],
                form_data["phosphorus"],
                form_data["potassium"],
            )
            pest_advice = pest_disease_advisory(crop, weather["humidity"], form_data["season"])
            explanation = build_explanation(crop, fertilizer, weather)

            advisory_id = save_advisory(
                user_id=session["user_id"],
                crop=crop,
                fertilizer=fertilizer,
                pest_advice=pest_advice,
                explanation=explanation,
                weather=weather,
                form_data=form_data,
            )

            return render_template(
                "advisory_result.html",
                advisory=get_advisory(advisory_id),
            )

        return render_template("advisory_form.html")

    @app.route("/history")
    @login_required
    def history():
        items = get_user_advisories(session["user_id"])
        return render_template("history.html", items=items)

    return app


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS advisories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                location TEXT,
                soil_ph REAL,
                nitrogen REAL,
                phosphorus REAL,
                potassium REAL,
                season TEXT,
                temperature REAL,
                rainfall REAL,
                humidity REAL,
                crop TEXT,
                fertilizer TEXT,
                pest_advice TEXT,
                explanation TEXT,
                created_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """
        )
        conn.commit()


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model not found. Run `python app/ml/train_model.py` to train the model."
        )
    return joblib.load(MODEL_PATH)


def predict_crop(nitrogen, phosphorus, potassium, ph, rainfall, temperature, humidity):
    model = load_model()
    features = [[nitrogen, phosphorus, potassium, ph, rainfall, temperature, humidity]]
    return model.predict(features)[0]


def save_advisory(user_id, crop, fertilizer, pest_advice, explanation, weather, form_data):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO advisories (
                user_id, location, soil_ph, nitrogen, phosphorus, potassium, season,
                temperature, rainfall, humidity, crop, fertilizer, pest_advice, explanation, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                form_data["location"],
                form_data["soil_ph"],
                form_data["nitrogen"],
                form_data["phosphorus"],
                form_data["potassium"],
                form_data["season"],
                weather["temperature"],
                weather["rainfall"],
                weather["humidity"],
                crop,
                fertilizer,
                pest_advice,
                explanation,
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        return cursor.lastrowid


def get_advisory(advisory_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM advisories WHERE id = ?", (advisory_id,))
        row = cursor.fetchone()
    return row_to_dict(row)


def get_latest_advisory(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM advisories WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
            (user_id,),
        )
        row = cursor.fetchone()
    return row_to_dict(row) if row else None


def get_user_advisories(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM advisories WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,),
        )
        rows = cursor.fetchall()
    return [row_to_dict(row) for row in rows]


def row_to_dict(row):
    if not row:
        return None
    keys = [
        "id",
        "user_id",
        "location",
        "soil_ph",
        "nitrogen",
        "phosphorus",
        "potassium",
        "season",
        "temperature",
        "rainfall",
        "humidity",
        "crop",
        "fertilizer",
        "pest_advice",
        "explanation",
        "created_at",
    ]
    return dict(zip(keys, row))


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
