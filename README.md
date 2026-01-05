# 🥗 Smart Diet Planner (AI-Powered)

> A personalized health management platform that uses Machine Learning to generate disease-specific diet plans.

![Project Status](https://img.shields.io/badge/Status-In%20Development-orange)
![Python](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React.js-61DAFB)
![ML](https://img.shields.io/badge/Model-Random%20Forest-F7931E)

## 📖 Overview
The **Smart Diet Planner** is a web application designed to help patients manage chronic diseases (like Diabetes, Hypertension, PCOS) through proper nutrition. Unlike static diet sites, this project uses a **Random Forest Machine Learning model** to analyze user health data and predict the optimal diet type and daily calorie intake.

### 🌟 Key Features
- **User Authentication:** Secure Login/Signup using JWT (JSON Web Tokens).
- **Health Profiling:** Calculates BMI and categorizes users (Underweight, Obese, etc.).
- **Smart Predictions:** Predicts strict diet guidelines and foods to avoid based on disease.
- **Calorie Regression:** accurately estimates daily calorie requirements.
- **History Tracking:** Saves generated plans to the user's dashboard.

---

## 🏗️ Architecture & Tech Stack

The project follows a decoupled **Client-Server architecture** with a dedicated ML pipeline.

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| **Frontend** | React.js, Tailwind CSS | User Interface, Form Handling, Dashboard |
| **Backend** | Python, FastAPI | API Server, Auth Logic, Request Validation |
| **Database** | SQLite (Dev) / PostgreSQL | Storing User Credentials & Diet History |
| **ML Engine** | Scikit-Learn, Pandas | Random Forest Classifier & Regressor Models |

### 📂 Project Structure
```text
Diet_Planner_Project/
├── backend/            # FastAPI Server & Logic
│   ├── models/         # Database Tables & ML .pkl files
│   ├── auth/           # Login/Signup Logic
│   └── main.py         # Application Entry Point
├── frontend/           # React Application
│   ├── src/components  # UI Components
│   └── src/pages       # Login, Signup, Dashboard
└── training/           # ML Research Lab
    ├── data/           # Raw CSV Datasets
    └── train.py        # Script to train and save models
