import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# 1. Setup Safe File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "mldataset.csv")
model_path = os.path.join(BASE_DIR, "diet_classifier.pkl")

# 2. Load Data
print(f"📂 Loading dataset from: {csv_path}")
try:
    df = pd.read_csv(csv_path)
    print("✅ Dataset loaded successfully.")
except FileNotFoundError:
    print(f"❌ ERROR: Could not find file at {csv_path}")
    exit(1)

# 3. Encode Categorical Data
# We need to save these encoders so the backend can decode the predictions later!
encoders = {}
categorical_cols = ["Age_Group", "BMI_Category", "Disease", "Recommended_Diet", "Avoid_Food"]

for col in categorical_cols:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

# 4. Prepare Features (X) and Target (y)
X = df[["Age_Group", "BMI_Category", "Disease"]]
# We combine Diet and Avoid_Food into a single target list
y = list(zip(df["Recommended_Diet"], df["Avoid_Food"]))

# 5. Train Model
print("🧠 Training Random Forest Model...")
classifier = RandomForestClassifier(n_estimators=200, random_state=42)
classifier.fit(X, y)

# 6. Save Model AND Encoders
# We save a dictionary containing both the model and the translators (encoders)
print(f"💾 Saving model to: {model_path}")
data_to_save = {
    "model": classifier,
    "encoders": encoders
}

with open(model_path, "wb") as f:
    pickle.dump(data_to_save, f)

print("✅ Model and Encoders saved successfully!")