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

##  How to Run
pip install -r requirements.txt


## Interactive ML Visualization Dashboard

An interactive dashboard was added to improve anomaly monitoring, visualization, and interpretability of Aadhaar enrollment patterns using AI-assisted anomaly analytics.

### Features Added

* Isolation Forest based anomaly detection
* Interactive anomaly distribution visualization
* Correlation heatmaps for enrollment attributes
* Time-series anomaly trend analysis
* Pincode-wise suspicious activity monitoring
* Date range filtering for anomaly investigation
* Interactive suspicious records table

### Dashboard Analytics

#### Anomaly Distribution Visualization

Displays the ratio of normal vs suspicious enrollment records detected by the anomaly detection model, helping understand anomaly frequency within the dataset.

#### Correlation Heatmaps

Shows relationships between enrollment attributes and age-group patterns, helping identify feature dependencies and unusual enrollment behavior.

#### Time-Series Anomaly Trend Analysis

Visualizes suspicious enrollment activity across dates to identify sudden spikes, irregular surges, and abnormal enrollment behavior over time.

#### Pincode-wise Suspicious Activity Monitoring

Highlights which pincodes are showing higher suspicious enrollment behavior, helping identify region-specific anomalies and irregular activity patterns.

#### Date Range Filtering

Allows users to investigate suspicious activity within a selected time period for better temporal analysis and targeted anomaly monitoring.

#### Interactive Suspicious Records Table

Displays suspicious records along with important details such as date, state, district, pincode, and enrollment counts for detailed anomaly investigation and manual verification.

### Technologies Used

* Streamlit
* Plotly
* Seaborn
* Matplotlib
* Scikit-learn

### Run Interactive Dashboard

```bash id="r8wx2n"
cd Visuals
python -m streamlit run dashboard.py
```
