import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load labeled data
df = pd.read_csv("data/food_labeled.csv")

# Select features and label
X = df[["calories", "protein", "fat", "carbs", "fiber"]]
y = df["goal"]

# Encode labels (text → numbers)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train (THIS IS THE CORE ML STEP)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Save model & encoder
joblib.dump(model, "model/food_goal_model.pkl")
joblib.dump(label_encoder, "model/label_encoder.pkl")

print("✅ Model trained & saved successfully")
