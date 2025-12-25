import pandas as pd

food = pd.read_csv("data/usda/food.csv")
food_nutrient = pd.read_csv("data/usda/food_nutrient.csv")

NUTRIENTS = {
    1008: "calories",
    1003: "protein",
    1004: "fat",
    1005: "carbs",
    1079: "fiber"
}

food_nutrient = food_nutrient[
    food_nutrient["nutrient_id"].isin(NUTRIENTS.keys())
]


food_nutrient["nutrient_name"] = food_nutrient["nutrient_id"].map(NUTRIENTS)


pivot = food_nutrient.pivot_table(
    index="fdc_id",
    columns="nutrient_name",
    values="amount"
).reset_index()

final = pivot.merge(
    food[["fdc_id", "description"]],
    on="fdc_id",
    how="left"
)
final.rename(columns={"description": "food_name"}, inplace=True)

final = final.dropna(subset=["calories"])

final.to_csv("data/food_nutrition.csv", index=False)

print("✅ food_nutrition.csv created")
print(final.head())

