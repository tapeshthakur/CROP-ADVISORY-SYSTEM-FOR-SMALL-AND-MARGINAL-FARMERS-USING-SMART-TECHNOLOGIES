# Crop Advisory System for Small and Marginal Farmers

A smart, farmer-friendly crop advisory platform that provides crop recommendations, fertilizer guidance, pest/disease alerts, and weather-based tips using machine learning.

## ✨ Features
- Farmer/Admin registration and login.
- Input soil parameters (N, P, K, pH), location, and season.
- Weather integration via OpenWeatherMap API (mock data fallback).
- Crop recommendation using a Random Forest model.
- Fertilizer recommendation based on nutrient gaps.
- Basic pest and disease advisory.
- Dashboard with latest advisory insights.
- History of past advisories per farmer.

## 📁 Project Structure
```
CROP-ADVISORY-SYSTEM-FOR-SMALL-AND-MARGINAL-FARMERS-USING-SMART-TECHNOLOGIES/
├── app/
│   ├── app.py
│   ├── __init__.py
│   ├── data/
│   │   └── crop_recommendation_sample.csv
│   ├── db/
│   │   └── schema.sql
│   ├── ml/
│   │   └── train_model.py
│   ├── static/
│   │   └── css/
│   │       └── styles.css
│   ├── templates/
│   │   ├── advisory_form.html
│   │   ├── advisory_result.html
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   ├── index.html
│   │   ├── login.html
│   │   └── register.html
│   └── utils/
│       ├── __init__.py
│       ├── advisory.py
│       └── weather.py
├── requirements.txt
└── README.md
```

## 🧠 Machine Learning Workflow
1. **Data preprocessing:** use the sample dataset in `app/data`.
2. **Training:** run `python app/ml/train_model.py` to train a Random Forest model.
3. **Model storage:** the script saves the model as `app/ml/model.pkl`.
4. **Prediction:** the Flask app loads the model and predicts the best crop.

## 🗄️ Database Schema
The SQLite schema is defined in `app/db/schema.sql` and automatically created on first run. It stores:
- Users (username, password, role)
- Advisories (soil data, weather, crop, fertilizer, and explanations)

## ⚙️ Setup Instructions
### 1. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the ML model
```bash
python app/ml/train_model.py
```

### 4. Run the Flask application
```bash
python app/app.py
```

Open the app in your browser at: `http://localhost:5000`

## 🌦️ Weather API (Optional)
Set the OpenWeatherMap API key to fetch live weather:
```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```
If not set, the app uses realistic mock weather values.

## 🚀 Future Scope
- Integrate satellite imagery and IoT sensors.
- Support regional language translations.
- Add SMS/WhatsApp advisory delivery.
- Provide advanced pest detection using computer vision.

## ✅ Academic Suitability
The project is modular, well-commented, and includes machine learning, database integration, and UI components suitable for academic submission.
