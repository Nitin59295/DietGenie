from flask import Blueprint, request, jsonify
from services.ml_service import predict_food_goal,generate_day_plan,recommend_foods


ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/predict-food-goal", methods=["POST"])
def predict_food():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    required = ["calories", "protein", "fat", "carbs", "fiber"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing nutrition values"}), 400

    goal = predict_food_goal(
        calories=float(data["calories"]),
        protein=float(data["protein"]),
        fat=float(data["fat"]),
        carbs=float(data["carbs"]),
        fiber=float(data["fiber"])
    )

    return jsonify({
        "predicted_goal": goal
    })

@ai_bp.route("/recommend-meal", methods=["POST"])
def recommend_meal():
    data = request.get_json()
    if not data or "goal" not in data:
        return jsonify({"error": "Diet goal required"}), 400

    goal = data["goal"]
    max_calories = data.get("max_calories", 300)

    foods = recommend_foods(
        goal=goal,
        max_calories=int(max_calories)
    )

    return jsonify({
        "goal": goal,
        "recommendations": foods
    })
@ai_bp.route("/generate-day-plan", methods=["POST"])
def generate_day_plan_api():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    if "goal" not in data or "daily_calories" not in data:
        return jsonify({"error": "goal and daily_calories required"}), 400

    plan = generate_day_plan(
        goal=data["goal"],
        daily_calories=int(data["daily_calories"])
    )

    return jsonify(plan)
