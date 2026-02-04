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
