# CMSE830
# FIFA World Cup 2022: Weather & Match Performance Analysis  

### By: Samarth Rao  
**Course:** CMSE 830 — Fall 2025  

---

## Project Overview  
This project explores how **temperature** and **humidity** conditions in Qatar during the 2022 FIFA World Cup affected player performance.  
It combines **official match statistics** with **daily weather data** and applies basic data cleaning, imputation, and exploratory data analysis.

The final output is an **interactive Streamlit dashboard** that visualizes how climate factors relate to scoring, attempts, and accuracy — along with a custom **Climate Impact Score** that summarizes environmental influence on gameplay.

---

## Files in This Repository

| File | Description |
|------|--------------|
| `Fifa_world_cup_matches.csv` | Raw match-level dataset with goals, attempts, and on-target shots |
| `qatar_weather.csv` | Weather data for Qatar during the tournament |
| `Midsem_project_code.py` | Main Python analysis script (data cleaning, merging, imputation, EDA, and derived metrics) |
| `app.py` | Streamlit dashboard for interactive visualization |
| `README.md` | Project documentation |

---

## ⚙️ Setup Instructions  

### 1. Clone the Repository  
```bash
git clone https://github.com/<your-username>/fifa-weather-analysis.git
cd fifa-weather-analysis
