# ==============================
# FIFA World Cup Weather Dashboard
# Author: Samarth Rao
# ==============================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="FIFA Weather Dashboard", layout="wide")

# ==============================
# 1) Load Data
# ==============================
@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_fifa_weather_advanced.csv")
    return df

@st.cache_data
def load_missingness():
    try:
        miss = pd.read_csv("missingness_summary.csv")
        return miss
    except:
        return None

data = load_data()
missingness = load_missingness()

# ==============================
# 2) Header
# ==============================
st.title("🏆 FIFA World Cup 2022 — Weather & Performance Dashboard")
st.markdown("""
This dashboard explores how **temperature** and **humidity** affected match performance
during the 2022 FIFA World Cup in Qatar.  
It also introduces a custom *Climate Impact Score* combining both factors.

---
""")

# ==============================
# 3) Sidebar Filters
# ==============================
st.sidebar.header("🎛️ Filters")

temp_range = st.sidebar.slider(
    "Temperature Range (°F)",
    float(data["temp"].min()), float(data["temp"].max()),
    (float(data["temp"].min()), float(data["temp"].max()))
)

humidity_range = st.sidebar.slider(
    "Humidity Range (%)",
    float(data["humidity"].min()), float(data["humidity"].max()),
    (float(data["humidity"].min()), float(data["humidity"].max()))
)

metric = st.sidebar.selectbox(
    "Select Performance Metric",
    ["avg_goals", "avg_attempts", "avg_on_target"],
    format_func=lambda x: x.replace("_", " ").title()
)

show_table = st.sidebar.checkbox("Show Summary Table", value=False)

filtered = data[
    (data["temp"].between(*temp_range)) &
    (data["humidity"].between(*humidity_range))
]

st.success(f"Showing {len(filtered)} matches within selected range")

# ==============================
# 4) Visuals
# ==============================
col1, col2 = st.columns(2)

# left — climate score vs metric
with col1:
    st.subheader(f"{metric.replace('_', ' ').title()} vs Climate Impact Score")
    fig, ax = plt.subplots()
    ax.scatter(filtered["climate_impact_score"], filtered[metric], color="#6C63FF", alpha=0.8, edgecolor="black", linewidth=0.5)
    if len(filtered) > 1:
        m, b = np.polyfit(filtered["climate_impact_score"], filtered[metric], 1)
        ax.plot(filtered["climate_impact_score"], m*filtered["climate_impact_score"]+b, color="black")
    ax.set_xlabel("Climate Impact Score (0–1)")
    ax.set_ylabel(metric.replace("_", " ").title())
    ax.grid(True, linestyle="--", alpha=0.4)
    st.pyplot(fig)

# right — temp vs humidity colored
with col2:
    st.subheader("Temperature vs Humidity (colored by performance)")
    fig2, ax2 = plt.subplots()
    sc = ax2.scatter(filtered["temp"], filtered["humidity"], c=filtered[metric], cmap="coolwarm", s=70, alpha=0.8, edgecolor="black")
    cbar = plt.colorbar(sc, ax=ax2)
    cbar.set_label(metric.replace("_", " ").title())
    ax2.set_xlabel("Temperature (°F)")
    ax2.set_ylabel("Humidity (%)")
    ax2.grid(True, linestyle="--", alpha=0.4)
    st.pyplot(fig2)

# ==============================
# 4.5) Missingness Viz
# ==============================
st.markdown("---")
st.subheader("🩹 Missing Data Overview")

if missingness is None:
    st.warning("Missingness summary not found. Run preprocessing first.")
else:
    miss = missingness[missingness["missing_count"] > 0]
    if miss.empty:
        st.info("No missing values detected.")
    else:
        fig_miss, ax_miss = plt.subplots()
        ax_miss.barh(miss["column"], miss["missing_count"], color="#FFB347")
        ax_miss.set_xlabel("Missing Count")
        ax_miss.set_ylabel("Column")
        ax_miss.set_title("Missingness Before Imputation")
        for i, v in enumerate(miss["missing_count"]):
            ax_miss.text(v + 0.2, i, str(v), va="center", fontsize=8)
        st.pyplot(fig_miss)

# ==============================
# 5) Boxplot
# ==============================
st.markdown("---")
st.subheader(f"Distribution of {metric.replace('_', ' ').title()} by Temperature Group")

fig3, ax3 = plt.subplots()
filtered.boxplot(column=metric, by="temp_group", grid=False, patch_artist=True, ax=ax3)
colors = ["#FF9999", "#66B3FF"]
for patch, color in zip(ax3.artists, colors):
    patch.set_facecolor(color)
ax3.set_xlabel("Temperature Group")
ax3.set_ylabel(metric.replace("_", " ").title())
plt.suptitle("")
st.pyplot(fig3)

# ==============================
# 6) Optional Summary Table
# ==============================
if show_table:
    st.markdown("---")
    st.subheader("📊 Summary Statistics")
    st.dataframe(filtered[[metric, "temp", "humidity", "climate_impact_score"]].describe())

# ==============================
# 7) Footer
# ==============================
st.markdown("""
---
### 💡 Observations
- Performance slightly drops under hotter and more humid conditions.  
- The *Climate Impact Score* summarizes this effect neatly.  
- Weather shows measurable, if subtle, impact on match quality.

---
**Developed by:** Samarth Rao  
**Course:** CMSE 830 — Fall 2025  
""")
