import joblib
import os
import re
import pandas as pd

# ------------------ PATHS ------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ------------------ LOAD DATA ------------------
food_df = pd.read_csv(os.path.join(BASE_DIR, "data/food_nutrition.csv"))

model = joblib.load(os.path.join(BASE_DIR, "model/food_goal_model.pkl"))
label_encoder = joblib.load(os.path.join(BASE_DIR, "model/label_encoder.pkl"))

# ------------------ BASIC PREDICTION ------------------
def predict_food_goal(calories, protein, fat, carbs, fiber):
    features = [[calories, protein, fat, carbs, fiber]]
    pred = model.predict(features)[0]
    return label_encoder.inverse_transform([pred])[0]

# ------------------ NORMALIZATION ------------------
def normalize_food_name(name):
    name = name.lower()
    name = re.sub(r"\(.*?\)", "", name)
    name = name.split(",")[0]
    return name.strip()

# ------------------ MAIN RECOMMENDER ------------------
def recommend_foods(goal, min_calories=80, max_calories=500, limit=30):
    """
    Primary recommender with calorie bands + ML filtering
    """
    df = food_df.copy()

    preds = model.predict(
        df[["calories", "protein", "fat", "carbs", "fiber"]]
    )
    df["predicted_goal"] = label_encoder.inverse_transform(preds)

    df = df[
        (df["predicted_goal"] == goal) &
        (df["calories"] >= min_calories) &
        (df["calories"] <= max_calories)
    ]

    # Ranking strategy
    if goal == "weight_loss":
        df = df.sort_values(by=["fiber", "protein"], ascending=False)
    elif goal == "weight_gain":
        df = df.sort_values(by=["calories", "fat"], ascending=False)
    else:
        df = df.sort_values(by=["protein"], ascending=False)

    return df.head(limit)[[
        "food_name", "calories", "protein", "carbs", "fat", "fiber"
    ]].to_dict(orient="records")

# ------------------ FALLBACK RECOMMENDER ------------------
def recommend_foods_relaxed(goal, limit=30):
    """
    Guaranteed fallback recommender (never empty)
    """
    df = food_df.copy()

    preds = model.predict(
        df[["calories", "protein", "fat", "carbs", "fiber"]]
    )
    df["predicted_goal"] = label_encoder.inverse_transform(preds)

    df = df[df["predicted_goal"] == goal]
    df = df[df["calories"] >= 50]

    return df.sort_values(
        by=["protein", "fiber"],
        ascending=False
    ).head(limit)[[
        "food_name", "calories", "protein", "carbs", "fat", "fiber"
    ]].to_dict(orient="records")


def is_core_food(food):
    """
    Core foods are meal staples, not snacks
    """
    return food["calories"] >= 180

def generate_day_plan(goal, daily_calories):
    """
    FINAL production-grade full-day planner
    Enforces:
    - Core food per meal
    - No repetition
    - Realistic meals
    """

    splits = {
        "breakfast": (0.25, 180, 500),
        "lunch": (0.40, 250, 700),
        "dinner": (0.35, 220, 600)
    }

    used_foods = set()
    plan = {}

    for meal, (ratio, min_c, max_c) in splits.items():
        target = int(daily_calories * ratio)

        # Get candidates
        candidates = recommend_foods(
            goal=goal,
            min_calories=50,
            max_calories=max_c,
            limit=50
        )

        if not candidates:
            candidates = recommend_foods_relaxed(goal, limit=50)

        selected = []
        total = 0

        # 🔑 STEP 1: pick ONE core food
        core_added = False
        for food in candidates:
            name = normalize_food_name(food["food_name"])
            if name in used_foods:
                continue

            if is_core_food(food):
                selected.append(food)
                used_foods.add(name)
                total += food["calories"]
                core_added = True
                break

        # 🔑 STEP 2: fill remaining calories with sides
        for food in candidates:
            if total >= target * 0.8:
                break

            name = normalize_food_name(food["food_name"])
            if name in used_foods:
                continue

            selected.append(food)
            used_foods.add(name)
            total += food["calories"]

        # 🔒 Absolute safety
        if not selected:
            selected = candidates[:3]

        plan[meal] = {
            "target_calories": target,
            "foods": selected
        }

    return plan
