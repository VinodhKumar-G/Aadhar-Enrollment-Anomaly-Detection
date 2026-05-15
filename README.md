# 🆔 Aadhaar Enrollment Anomaly Detection

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![GSSoC 2026](https://img.shields.io/badge/GSSoC-2026-orange)](https://gssoc.girlscript.tech/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-assisted analytical system to detect trends and anomalies in public Aadhaar enrollment data, focusing on sustainable digital governance in Bengaluru Rural.

---

## 🚀 The Vision
Sudden drops or spikes in enrollment often go unnoticed. This project fills that gap by using **Explainable AI (XAI)**—specifically statistical anomaly detection (Z-score)—to provide proactive insights for government infrastructure planning.

## ✨ Key Features
- **Trend Analysis:** Automated monthly growth tracking across 0-5, 5-17, and 18+ age groups.
- **Anomaly Detection:** Statistical identification of irregular enrollment patterns using Z-score logic.
- **Transparent Logic:** No black-box models; strictly interpretable and ethical AI.
- **Sustainability Impact:** Supporting **SDG 11** by reducing regional service inequalities.

## 🛠️ Tech Stack
- **Languages:** Python
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, SciPy
- **Platform:** Jupyter Notebooks

## 📂 Project Structure
```text
├── Data/           # Publicly aggregated CSV datasets
├── Notebook/       # Core analysis logic (Analysis.ipynb)
├── Visuals/        # Generated trend plots and heatmaps
├── requirements.txt # Project dependencies
└── README.md
