# 💳 Credit Card Eligibility Prediction using Machine Learning

An end-to-end **Machine Learning + Streamlit web application** that predicts whether a customer is **eligible for a credit card** based on demographic and financial information.  
The application features a **banking-grade UI**, mandatory field validation, and multiple themes (Banking, FinTech, Dark).

---

## 🚀 Project Overview

Credit card eligibility evaluation is a critical task for banks and financial institutions.  
Manual screening is time-consuming, inconsistent, and prone to human bias.

This project automates the decision process using a **Machine Learning classification model** trained on historical customer data to deliver **fast, consistent, and data-driven eligibility predictions**.

---

## 🎯 Problem Statement

**To build a Machine Learning model that predicts whether a customer is eligible for a credit card based on customer demographics, account details, and transaction behavior.**

---

## 🧠 Solution Approach

1. Understand the banking and credit domain
2. Preprocess and analyze customer data
3. Perform feature selection to identify key predictors
4. Train a Machine Learning classification model
5. Build an interactive Streamlit web interface
6. Deploy the model for real-time eligibility prediction

---

## 📊 Dataset Information

- **Records:** 10,000+ customer entries  
- **Features:** 16 input variables  
- **Target Variable:** Credit Card Eligibility (Eligible / Not Eligible)

### Key Features Used
- Customer Age  
- Gender  
- Income Category  
- Credit Limit  
- Total Transaction Amount  
- Total Transaction Count  
- Average Utilization Ratio  
- Months on Book  
- Total Relationship Count  

---

## ⚙️ Machine Learning Model

- **Algorithm:** Decision Tree Classifier  
- **Problem Type:** Binary Classification  

### Why Decision Tree?
- Captures non-linear decision rules
- Easy to interpret
- Suitable for credit risk decision logic

### Evaluation Metrics
- Accuracy
- Precision
- Recall
- Confusion Matrix

---

## 🖥️ Streamlit Web Application

### Application Features
- Clean and professional banking-style UI
- Mandatory input validation (required fields marked with *)
- Multiple UI themes:
  - 🟢 Banking Theme
  - 🟣 FinTech Theme
  - 🌙 Dark Theme
- Real-time eligibility prediction
- Clear success and rejection messages

---

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **Machine Learning:** Scikit-learn  
- **Web Framework:** Streamlit  
- **Numerical Computing:** NumPy  
- **Model Serialization:** Pickle  

---

## 📁 Project Structure

