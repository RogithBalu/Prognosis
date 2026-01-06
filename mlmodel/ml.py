import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

df = pd.read_csv("mldataset.csv")

print("Missing values:")
print(df.isnull().sum())


encoders = {}

categorical_cols = [
    "Age_Group",
    "BMI_Category",
    "Disease",
    "Recommended_Diet",
    "Avoid_Food"
]

for col in categorical_cols:
    le = LabelEncoder()
    df[col]=le.fit_transform(df[col])
    encoders[col]=le

print("\nEncoded feature sample:")
print(df[["Age_Group", "BMI_Category", "Disease"]].head())


X=df[["Age_Group", "BMI_Category", "Disease"]]

y=list(zip(df["Recommended_Diet"], df["Avoid_Food"]))


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


classifier = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

classifier.fit(X_train, y_train)


y_pred = classifier.predict(X_test)


correct = sum(
    1 for yt, yp in zip(y_test, y_pred)
    if tuple(yt) == tuple(yp)
)

accuracy = correct / len(y_test)

print("\nExact Match Accuracy:", accuracy)


with open("diet_classifier.pkl", "wb") as f:
    pickle.dump(
        {
            "model": classifier,
            "encoders": encoders
        },
        f
    )

print("\nDiet classifier trained and saved successfully")


sample = [[
    encoders["Age_Group"].transform(["Adult"])[0],
    encoders["BMI_Category"].transform(["Overweight"])[0],
    encoders["Disease"].transform(["Diabetes"])[0]
]]

pred = classifier.predict(sample)

diet = encoders["Recommended_Diet"].inverse_transform([pred[0][0]])[0]
avoid = encoders["Avoid_Food"].inverse_transform([pred[0][1]])[0]

print("\nSample Prediction:")
print("Predicted Diet:", diet)
print("Avoid Food:", avoid)

