# Fintech-Fraud-Detection-System

A fraud detection engine that models individual user transaction patterns and detects anomalies using behavioral deviation and geospatial intelligence.

---

## 📌 Project Overview

This system simulates a production-style fintech fraud engine that:

- Learns personalized user behavior baselines
- Detects transaction anomalies
- Identifies geospatial inconsistencies
- Flags impossible travel scenarios
- Generates explainable risk scores
- Works in real-time via CLI

The model is unsupervised and does not rely on fraud labels.

---

## 🧠 Core Features

### 1. Behavioral Modeling
- User-level average transaction amount
- Standard deviation-based anomaly detection
- Hour-of-day behavior deviation

### 2. Geospatial Intelligence
- Haversine distance calculation
- Location deviation scoring
- Travel speed estimation
- Impossible travel detection (> 900 km/h)

### 3. Hybrid Risk Scoring
- Weighted anomaly aggregation
- Continuous risk score (0–1)
- Risk classification (LOW, MEDIUM, HIGH, CRITICAL)
- Explainable risk drivers

---

## ⚙️ Installation

1. Create virtual environment (recommended):

        python -m venv venv
        venv\Scripts\activate


2. Install dependencies:

        pip install -r requirements.txt


---

## 🚀 Running the System

1. Start the CLI engine:

        python main.py

---

## 🔍 How It Works

1. Historical transaction data builds user profiles.
2. New transactions are compared against baseline behavior.
3. Deviation features are generated.
4. Rule-based weighted scoring calculates risk.
5. Structured, explainable output is produced.

---

## 🎯 Purpose

This project demonstrates behavioral anomaly detection, geospatial risk modeling, hybrid rule engines, and production-style fraud scoring design suitable for fintech environments.
