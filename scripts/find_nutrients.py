import pandas as pd

nutrient = pd.read_csv("data/usda/nutrient.csv")

targets = [
    "Energy",
    "Protein",
    "Total lipid (fat)",
    "Carbohydrate, by difference",
    "Fiber, total dietary"
]

filtered = nutrient[nutrient["name"].isin(targets)]

print(filtered[["id", "name", "unit_name"]])
