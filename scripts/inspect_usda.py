import pandas as pd


base_path = "data/usda/"

food = pd.read_csv(base_path + "food.csv")
nutrient=pd.read_csv(base_path + "nutrient.csv")
food_nutrient=pd.read_csv(base_path + "food_nutrient.csv")

print("Food:", food.shape)
print("Nutrient:", nutrient.shape)
print("Food_Nutrient:", food_nutrient.shape)

print(food.head())
print(nutrient.head())
print(food_nutrient.head())
