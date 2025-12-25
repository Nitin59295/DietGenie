#THIS IS LABELING (converting Human logic -> AI )
#Before training, you must decide:
#What is the output (label)?

import pandas as pd

df = pd.read_csv("data/food_nutrition.csv")

def label_food(row):
    if row["calories"]<120 and row["fiber"] >=3:
        return "weight_loss"
    elif row["calories"] > 250:
        return "weight_gain"
    else:
        return "maintenance"
    
df["goal"] = df.apply(label_food,axis=1)
df.to_csv("data/food_labeled.csv", index=False)

print(df["goal"].value_counts())
print("food_labeled.csv created")