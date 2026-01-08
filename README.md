# Brand Reputation Intelligence & Sentiment Trend Analysis

## Overview
This project develops an end-to-end brand sentiment intelligence system designed to monitor public perception, detect emerging reputational risks and surface actionable insights from large-scale social media data. The solution integrates transformer-based NLP modeling with an interactive analytics dashboard to support continuous sentiment monitoring.

## Objective
Brands face rapid sentiment shifts driven by customer feedback and engagement dynamics. This project aims to:
- Classify sentiment at scale using deep learning–based NLP models
- Track sentiment trends and engagement spikes over time
- Identify early indicators of reputational risk from social media signals

## Data & Scope
- Fine-tuned on approximately **30,000 tweets** spanning three sentiment classes
- Applied inference on **~5,000 brand-specific tweets** for trend and risk analysis
- Focused on temporal sentiment movement and engagement-driven anomalies

## Methodology
- Implemented a transformer-based sentiment classification pipeline using **DistilBERT**
- Performed text preprocessing, tokenization, model training and evaluation workflows
- Achieved **88.9% classification accuracy** across sentiment classes
- Applied trained models to brand-specific datasets to analyze sentiment shifts and engagement correlations

## Analytics & Visualization
- Developed an interactive **Streamlit dashboard** to visualize:
  - Sentiment trends over time
  - Engagement spikes aligned with sentiment changes
  - Emerging reputational risk patterns
- Enabled exploratory analysis to support timely brand insight generation

## System Components
- **NLP Modeling:** Transformer-based sentiment classification (DistilBERT)
- **Data Processing:** Python-based preprocessing and inference pipelines
- **Dashboard:** Streamlit application for real-time sentiment analytics

## Tools & Technologies
- Python
- Pandas, NumPy
- Scikit-learn
- Hugging Face Transformers (DistilBERT)
- Natural Language Processing (NLP)
- Streamlit

## Repository Notes
Raw and processed datasets are excluded due to size considerations. The repository focuses on modeling logic, analytical workflows and visualization outputs.

