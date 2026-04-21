# 💳 Credit Card Eligibility Prediction System

An end-to-end Machine Learning project that predicts whether a customer is eligible for a credit card based on financial and behavioral attributes. The system is deployed as an interactive web application using Streamlit, simulating a real-world banking credit decision workflow.

---

## 📌 Project Overview

This project builds a complete ML pipeline starting from raw banking data to a deployed application. The model analyzes customer demographics, transaction behavior, and credit usage patterns to determine eligibility.

---

## 📊 Dataset

- ~10,000+ customer records  
- Includes **16+ features** such as:
  - Customer Age  
  - Income Category  
  - Credit Limit  
  - Transaction Amount & Count  
  - Credit Utilization Ratio  
  - Account Tenure  
  - Relationship Count  

- Target Variable:
  - `credit_limit_eligible`  
    - **1 → Eligible (Existing Customer)**  
    - **0 → Not Eligible (Attrited Customer)**  

---

## ⚙️ Project Workflow

### 1. Data Preprocessing
- Removed irrelevant and redundant columns  
- Handled missing values and duplicates  
- Feature engineering for target variable  
- Encoded categorical features using **OrdinalEncoder**  
- Scaled numerical features using **StandardScaler**

---

### 2. Exploratory Data Analysis (EDA)
- Box plots for outlier detection  
- Count plots for categorical distributions  
- Correlation heatmap for feature relationships  
- Identified **class imbalance (~85% vs ~15%)**

---

### 3. Model Building

Trained and compared multiple models:

- K-Nearest Neighbors (KNN)  
- Logistic Regression  
- Gaussian Naive Bayes  
- Decision Tree  
- **Random Forest (Final Model)**  

---

## 🏆 Model Performance

- **Best Model:** Random Forest  
- **Accuracy Achieved:** **95.85%**  
- Selected based on highest performance and ability to handle feature interactions effectively  

---

## 🌐 Deployment (Streamlit App)

The model is deployed using Streamlit with a professional UI:

### Features:
- Real-time eligibility prediction  
- Structured input form with validation  
- Dynamic result display (Approved / Rejected)  
- Clean banking-style user interface  

---

## 💡 Explainability Feature

Implemented a **rule-based feedback system** that:

- Provides **top 3 personalized rejection reasons**  
- Explains decisions based on:
  - Transaction behavior  
  - Credit utilization  
  - Income category  
  - Account activity  

👉 This simulates real-world banking decision transparency.

---

## 🛠️ Tech Stack

- **Programming:** Python  
- **Libraries:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn  
- **Modeling:** Machine Learning (Classification)  
- **Deployment:** Streamlit  
- **Version Control:** Git & GitHub  

---

## 📂 Project Structure
