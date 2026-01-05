# 🏥 PrediCare: AI-Powered Disease Prediction System

![Python](https://img.shields.io/badge/Python-3.9-blueviolet)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68-green)
![Scikit-Learn](https://img.shields.io/badge/Sklearn-Modeling-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 📖 Overview
**PrediCare** is a machine-learning-based healthcare system designed to assist users and medical professionals in identifying potential diseases based on symptoms. 

Unlike simple diagnostic tools, PrediCare goes a step further by providing a **comprehensive medical report** that includes:
* **Disease Prediction:** Identifies the disease with high accuracy using a Random Forest algorithm.
* **Description:** A concise explanation of the condition.
* **Dietary Recommendations:** Personalized food lists to aid recovery.
* **Precautionary Measures:** Immediate steps to take (e.g., "See a doctor," "Rest").
* **Medication Suggestions:** Common drugs used for the condition (for reference only).

---

## 🚀 Features
* **Multi-Symptom Analysis:** Supports 132+ distinct symptoms (e.g., *itching, skin_rash, high_fever*).
* **High Accuracy:** Trained on a verified dataset of 4,920 medical records across 41 unique diseases.
* **FastAPI Backend:** Lightweight and ultra-fast REST API response (<50ms latency).
* **Robust ML Pipeline:** Uses a `RandomForestClassifier` with pre-trained vectors for instant inference.
* **Scalable Architecture:** Modular codebase allowing easy addition of new diseases or symptoms.

---

## 🛠️ Tech Stack
* **Backend:** FastAPI (Python)
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Data Processing:** Pickle (for model serialization)
* **Dataset:** 41 Diseases / 4,920 Patient Records

---

## 📂 Project Structure
```bash
├── data/
│   ├── Training.csv          # Main dataset
│   ├── description.csv       # Disease descriptions
│   ├── diets.csv             # Dietary recommendations
│   ├── medications.csv       # Medicine info
│   └── precautions_df.csv    # Precautions
├── models/
│   └── rf_model.pkl          # Serialized ML model
├── main.py                   # FastAPI Application Entry Point
├── predictor.py              # ML Logic & Inference Class
├── requirements.txt          # Python Dependencies
└── README.md