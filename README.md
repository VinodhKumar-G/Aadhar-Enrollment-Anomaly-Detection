# Aadhaar Enrollment Trend & Anomaly Detection  
AI-assisted trend and anomaly analysis of public Aadhaar enrollment data for sustainable digital governance.

The project analyses **public Aadhaar enrollment data** for **Bengaluru Rural district, Karnataka** indentifying the longterm trends and detect anomalies using **AI-assisted statistical methods**.

The goal is **sustainable digital governance** through data-driven, transparent, and responsible AI.

## Project Context
UIDAI Aadhar enrollment services generates a very large volume of data over time.However, **sudden drops, spikes, or irregular patterns** in enrollment process go unnoticed when monitoring is manual or get delayed.

Project identifies the gap by building an **AI-assisted analytical decision-support system** that automatically highlights the trends and anomalies to support the proactive governance using the insghts.

### Problem Statement
Uneven and unpredictable Aadhaar enrollment patterns can impact equitable access to digital identity services.  
Without automated analysis, anomalies may delay administrative response and affect service availability, especially in rural regions.

## Role of AI
AI is used in the form of **statistical pattern and anomaly detection**, which is a valid and explainable AI approach for analytical decision-support systems.

Key AI components:
- Automated trend analysis over time
- Statistical anomaly detection using Z-score
- Scalable and repeatable pattern identification
- Transparent and interpretable logic (no black-box models)

Advanced generative AI models (LLMs, RAG, Agentic AI) were intentionally not used to ensure **responsibility, explainability, and ethical compliance**.

## System Architecture

The following diagram illustrates the workflow and architecture of the Aadhaar Enrollment Anomaly Detection system.

![System Architecture](images/Architecture-diagram.png)

## 📊 Dataset
- Source: Publicly available, aggregated Aadhaar enrollment statistics
- Region: Bengaluru Rural district, Karnataka
- Granularity: Monthly
- Attributes:
  - Age 0–5
  - Age 5–17
  - Age 18+
- No personal, biometric, or sensitive data is used

## 🛠️ Methodology
1. Data loading and validation  
2. Date cleaning and preprocessing  
3. Feature engineering (total enrollment, growth rate)  
4. Trend analysis (overall and age-wise)  
5. AI-assisted anomaly detection (Z-score)  
6. Visualization and interpretation  

## 🌍 Sustainability Impact (SDG 11)
If implemented, this solution can:
- Enable early detection of service delivery issues
- Support better planning of enrollment infrastructure
- Reduce regional and demographic inequalities
- Improve access to digital identity for citizens

## ⚖️ Responsible AI Considerations
- Uses only aggregated and anonymized public data
- No surveillance, profiling, or personal data usage
- Transparent and explainable analytical logic
- Intended strictly for decision support


## 📂 Repository Structure

Aadhar-Enrollment-Anomaly-Detection
│
├── Data/ # Public dataset (CSV)
├── Notebook/ # Jupyter notebook analysis
│ └── Analysis.ipynb
├── Visuals/ # (Optional) Saved plots
├── README.md
├── requirements.txt
└── .gitignore

## 🚀 How to Run
pip install -r requirements.txt
