# 🥗 Diet Genie – ML-Powered Diet Planner

**Diet Genie** is a full-stack, ML-powered diet planning web application built with Flask.

It generates **goal-based diet plans** using a **custom-trained machine learning model** on USDA food data, with full **Docker support** for cross-platform deployment.

---

## 🚀 Key Highlights

- **ML-Based Food Classification**
    - Custom **RandomForest model (v1.0.0)**
    - Classifies foods into:
        - `weight_loss`
        - `maintenance`
        - `weight_gain`
- **BMI Calculator**
- **Full-Day Diet Planner**
    - Breakfast, Lunch, Dinner
    - Goal-based calorie distribution
- **Food Analyzer**
    - Predicts diet suitability of food items
- **PDF Diet Plan Export**
- **User Authentication**
    - Register / Login
    - Session-based access
- **Persistent Storage**
    - SQLite with Docker volume support
- **Dockerized Application**
    - Runs on macOS, Windows, Linux with zero setup

---

## 🧠 Machine Learning Details

- **Model**: RandomForestClassifier
- **Training Data**: USDA FoodData Central
- **Features Used**:
    - Calories
    - Protein
    - Fat
    - Carbohydrates
    - Fiber
- **Model Versioning**:
    - v1.0.0 released via **GitHub Releases**
- **Inference**:
    - Deterministic predictions
    - Rule-based constraints for meal realism

---

## 🧰 Tech Stack

### Backend

- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy

### Machine Learning

- scikit-learn
- pandas
- joblib

### Database

- SQLite

### PDF Generation

- WeasyPrint

### DevOps

- Docker
- Docker volumes (DB persistence)

---

## 📂 Project Structure

```
DietGenie/
├── app.py
├── Dockerfile
├── requirements.txt
├── extensions.py
├── models.py
│
├── services/
│   └── ml_service.py
│
├── routes/
│   ├── auth_routes.py
│   ├── bmi_routes.py
│   ├── diet_routes.py
│   ├── food_routes.py
│   └── ai_routes.py
│
├── data/
│   └── food_nutrition.csv
│
├── model/
│   ├── food_goal_model.pkl
│   └── label_encoder.pkl
│
├── instance/
│   └── calorie_app.db
│
├── templates/
│   └── *.html
│
├── static/
│   ├── css/
│   └── images/
└── README.md
```

---

## 🐳 Run with Docker (Recommended)

### 1️⃣ Build the image

```bash
docker build -t dietgenie .
```

### 2️⃣ Run the container (with DB persistence)

```bash
docker run -d \
  -p 5001:5000 \
  -v $(pwd)/instance:/app/instance \
  --name dietgenie_app \
  dietgenie
```

### 3️⃣ Initialize the database (first time only)

```bash
docker exec -it dietgenie_app flask init-db
```

### 4️⃣ Open in browser

```
http://localhost:5001
```

Register → Login → Use the app.

---

## 🧪 Run Without Docker (Optional)

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
flask init-db
python app.py
```

Runs at:

```
http://127.0.0.1:5000
```

---

## 📦 ML Model Releases

ML models are **versioned separately** via GitHub Releases.

- **Latest**: `v1.0.0`
- Includes:
    - `food_goal_model.pkl`
    - `label_encoder.pkl`

➡️ See **Releases** tab for downloadable artifacts.

---

## 🛣️ Roadmap

- ML model v2 (better food diversity)
- Weekly meal planner
- Nutrition explanation engine
- Admin dashboard
- Cloud deployment (Render / AWS)

---

## 👤 Author

**Nitin Bhatia**

MCA (AI & ML)

Python | Flask | Machine Learning | Docker

---

## ⭐ Final Note

This project follows **production-style ML lifecycle**:

- Trained model
- Versioned release
- Dockerized backend
- Persistent storage
- Deterministic inference
