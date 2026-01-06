import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

df=pd.read_csv("mldataset.csv")

print(df.head(10))
print("\nMissing values:")
print(df.isnull().sum())

disease_encoder=LabelEncoder()
bmi_encoder=LabelEncoder()
age_encoder=LabelEncoder()

df["Disease"]=disease_encoder.fit_transform(df["Disease"])
df["BMI_Category"]=bmi_encoder.fit_transform(df["BMI_Category"])
df["Age_Group"]=age_encoder.fit_transform(df["Age_Group"])

X = df[["Age_Group", "BMI_Category", "Disease"]]
y = df["Calories_per_day"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

regressor=RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

r2=r2_score(y_test, y_pred)
mae=mean_absolute_error(y_test, y_pred)
rmse=np.sqrt(mean_squared_error(y_test, y_pred))

print("\nModel Evaluation:")
print("R² Score:", r2)
print("Mean Absolute Error (MAE):", mae)
print("Root Mean Squared Error (RMSE):", rmse)

with open("calorie_regressor.pkl", "wb") as f:
    pickle.dump(
        {
            "model": regressor,
            "disease_encoder": disease_encoder,
            "bmi_encoder": bmi_encoder,
            "age_encoder": age_encoder
        },
        f
    )

print("\nCalorie Regressor trained and saved successfully")

sample = [[
    age_encoder.transform(["Adult"])[0],
    bmi_encoder.transform(["Overweight"])[0],
    disease_encoder.transform(["Diabetes"])[0]
]]

predicted_calories=regressor.predict(sample)

print("\nSample Prediction:")
print("Predicted Calories per day:", int(predicted_calories[0]))
