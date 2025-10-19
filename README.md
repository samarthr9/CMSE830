# CMSE 830 — Midsemester Project  
# FIFA World Cup 2022: Weather & Match Performance Analysis  

### By: Samarth Rao  
**Course:** CMSE 830 — Fall 2025  

---

## Project Overview  
This project investigates how **temperature** and **humidity** conditions in Qatar during the 2022 FIFA World Cup influenced player performance.  
It combines **official match data** with **daily weather records** and performs data cleaning, missing-value imputation, statistical testing, and exploratory data analysis.

The final deliverable is an **interactive Streamlit dashboard** that allows users to explore relationships between weather and gameplay metrics, alongside a custom **Climate Impact Score** summarizing environmental effects on match performance.

---

## Files in This Repository  

| File | Description |
|------|--------------|
| `Fifa_world_cup_matches.csv` | Raw match dataset containing goals, attempts, and accuracy per match |
| `qatar_weather.csv` | Raw weather data from Qatar during the World Cup |
| `Midsem_project_code.py` | Main Python script for data cleaning, merging, imputation, and statistical analysis |
| `app.py` | Streamlit dashboard for interactive exploration |
| `cleaned_fifa_weather.csv` | Cleaned version of merged match and weather data |
| `cleaned_fifa_weather_advanced.csv` | Final dataset with imputed values, outlier detection, and climate impact score |
| `missingness_summary.csv` | File summarizing missing values before imputation |
| `requirements.txt` | Python package dependencies required for running the project |
| `README.md` | Project documentation |

---

## Setup Instructions  

### 1. Clone the Repository  
```bash
git clone https://github.com/<samarthr9>/fifa-weather-analysis.git
cd fifa-weather-analysis
