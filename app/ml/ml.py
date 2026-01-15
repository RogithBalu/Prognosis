import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder  # 👈 THIS WAS MISSING
import pickle
import os

# Get the folder where THIS script (ml.py) lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the correct path to the CSV file
csv_path = os.path.join(BASE_DIR, "mldataset.csv")

# Load the dataset using the safe path
try:
    df = pd.read_csv(csv_path)
    print(f"✅ Loaded dataset from: {csv_path}")
except FileNotFoundError:
    print(f"❌ ERROR: Could not find file at {csv_path}")
    exit(1)

# ... (Rest of your code remains the same) ...
print(df.isnull().sum())

print(df.head(10))
encoders={}
categorical_cols=[
    "Age_Group",
    "BMI_Category",
    "Disease",
    "Recommended_Diet",
    "Avoid_Food"
]
for col in categorical_cols:
    le=LabelEncoder()
    df[col]=le.fit_transform(df[col])
    encoders[col]=le
print(df[["Age_Group", "BMI_Category", "Disease"]].head())

X = df[["Age_Group", "BMI_Category", "Disease"]]
y = list(zip(df["Recommended_Diet"], df["Avoid_Food"]))

classifier = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
classifier.fit(X, y)

with open("diet_classifier.pkl", "wb") as f:
    pickle.dump(
        {
            "model": classifier,
            "encoders": encoders
        },
        f
    )
    sample = [[
    encoders["Age_Group"].transform(["Adult"])[0],
    encoders["BMI_Category"].transform(["Overweight"])[0],
    encoders["Disease"].transform(["Diabetes"])[0]
]]

pred = classifier.predict(sample)

diet = encoders["Recommended_Diet"].inverse_transform([pred[0][0]])[0]
avoid = encoders["Avoid_Food"].inverse_transform([pred[0][1]])[0]

print("Predicted Diet:", diet)
print("Avoid Food:", avoid)


# ... (training code) ...

# Save the model using the safe path
model_path = os.path.join(BASE_DIR, "diet_classifier.pkl")

with open(model_path, "wb") as f:
    pickle.dump(clf, f)

print("✅ Diet classifier saved successfully")
