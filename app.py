import os
from flask import Flask
from dotenv import load_dotenv

from extensions import db, login_manager
from models import User

# Load environment variables
load_dotenv()

app = Flask(__name__)

# --- Instance folder for SQLite DB ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

# --- App Config ---
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "dev-secret-key-change-me"
)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(INSTANCE_DIR, 'calorie_app.db')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Initialize Extensions ---
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Register Blueprints ---
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.bmi_routes import bmi_bp
from routes.diet_routes import diet_bp
from routes.food_routes import food_bp
from routes.ai_routes import ai_bp
from routes.dashboard_routes import dashboard_bp

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(bmi_bp)
app.register_blueprint(diet_bp)
app.register_blueprint(food_bp)
app.register_blueprint(ai_bp, url_prefix="/ai")
app.register_blueprint(dashboard_routes := dashboard_bp)

# --- Auto-create DB tables (CRITICAL for Render) ---
with app.app_context():
    db.create_all()

# --- CLI Command (still useful locally) ---
@app.cli.command("init-db")
def init_db_command():
    """Initialize the database."""
    db.create_all()
    print("✅ Database initialized successfully")
