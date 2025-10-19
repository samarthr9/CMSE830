# =======================
# 0) Imports
# =======================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (8, 5)

# =======================
# 1) Load + basic clean
# =======================
game_data = pd.read_csv("/Users/samarthrao/Downloads/School/CMSE_830/Fifa_world_cup_matches.csv")
weather_data = pd.read_csv("/Users/samarthrao/Downloads/School/CMSE_830/qatar_weather.csv")

# dates
game_data["date_clean"] = pd.to_datetime(game_data["date"], errors="coerce")
weather_data["datetime"] = pd.to_datetime(weather_data["datetime"], errors="coerce")

# remove dupes if any
game_data = game_data.drop_duplicates()
weather_data = weather_data.drop_duplicates()

print("Game Data Shape:", game_data.shape)
print("Weather Data Shape:", weather_data.shape)

# =======================
# 2) Select + prep match metrics
# =======================
fifa_subset = game_data[[
    "date_clean",
    "number of goals team1", "number of goals team2",
    "total attempts team1", "total attempts team2",
    "on target attempts team1", "on target attempts team2"
]].copy()

# take averages for simplicity
fifa_averaged = fifa_subset.assign(
    avg_goals    = fifa_subset[["number of goals team1", "number of goals team2"]].mean(axis=1),
    avg_attempts = fifa_subset[["total attempts team1", "total attempts team2"]].mean(axis=1),
    avg_on_target= fifa_subset[["on target attempts team1", "on target attempts team2"]].mean(axis=1)
)[["date_clean", "avg_goals", "avg_attempts", "avg_on_target"]]

# =======================
# 3) Merge with weather
# =======================
combined_data = pd.merge(
    fifa_averaged,
    weather_data,
    left_on="date_clean",
    right_on="datetime",
    how="left"
)

# =======================
# 4) Handle Missing Values (clean + visual)
# =======================
print("\n=== Missing Values Before Imputation ===")
print(combined_data.isna().sum())

# store missingness summary (for Streamlit)
missing_summary = combined_data.isna().sum().reset_index()
missing_summary.columns = ["column", "missing_count"]
missing_summary.to_csv("missingness_summary.csv", index=False)

# calculate %
missing_percent = combined_data.isna().mean() * 100
print("\n% Missing by Column (>0):")
print(missing_percent[missing_percent > 0])

# basic approaches
mean_imputed = combined_data.copy()
for c in ["temp", "humidity"]:
    mean_imputed[c] = mean_imputed[c].fillna(mean_imputed[c].mean())

ffill_imputed = combined_data.copy()
for c in ["temp", "humidity"]:
    ffill_imputed[c] = ffill_imputed[c].fillna(method="ffill")

interp_imputed = combined_data.copy()
for c in ["temp", "humidity"]:
    interp_imputed[c] = interp_imputed[c].interpolate(method="linear")

print("\nAverage temp/humidity by method:")
print(pd.DataFrame({
    "Original":  combined_data[["temp", "humidity"]].mean(),
    "Mean":      mean_imputed[["temp", "humidity"]].mean(),
    "F-fill":    ffill_imputed[["temp", "humidity"]].mean(),
    "Interp":    interp_imputed[["temp", "humidity"]].mean()
}))

# interpolation makes sense for continuous time data
combined_data = interp_imputed
combined_data = combined_data.dropna(subset=["avg_goals", "avg_attempts", "avg_on_target"])

print("\n=== Missing Values After Imputation ===")
print(combined_data.isna().sum())

# quick temp plot (post-impute)
plt.figure(figsize=(8, 4))
plt.plot(combined_data["datetime"], combined_data["temp"], color="red", marker="o", label="Temperature")
plt.title("Temperature Over Time (After Imputation)")
plt.xlabel("Date")
plt.ylabel("Temperature (°F)")
plt.legend()
plt.tight_layout()
plt.show()

# =======================
# 5) Temp & humidity groups
# =======================
temp_cutoff = combined_data["temp"].median()
humidity_cutoff = combined_data["humidity"].median()

combined_data["temp_group"] = np.where(combined_data["temp"] >= temp_cutoff, "Hot", "Mild")
combined_data["humidity_group"] = np.where(combined_data["humidity"] >= humidity_cutoff, "Humid", "Dry")

# =======================
# 6) T-tests
# =======================
def run_t(metric):
    t1 = stats.ttest_ind(
        combined_data.loc[combined_data["temp_group"] == "Hot", metric],
        combined_data.loc[combined_data["temp_group"] == "Mild", metric],
        nan_policy="omit"
    )
    t2 = stats.ttest_ind(
        combined_data.loc[combined_data["humidity_group"] == "Humid", metric],
        combined_data.loc[combined_data["humidity_group"] == "Dry", metric],
        nan_policy="omit"
    )
    return t1, t2

for metric in ["avg_goals", "avg_attempts", "avg_on_target"]:
    t_temp, t_hum = run_t(metric)
    print(f"\n{metric.upper()} — Hot vs Mild: {t_temp}")
    print(f"{metric.upper()} — Humid vs Dry: {t_hum}")

# =======================
# 7) Correlations
# =======================
for m in ["avg_goals", "avg_attempts", "avg_on_target"]:
    r1, p1 = stats.pearsonr(combined_data["temp"], combined_data[m])
    r2, p2 = stats.pearsonr(combined_data["humidity"], combined_data[m])
    print(f"\n{m.upper()} correlations:")
    print(f"Temp: r={r1:.3f}, p={p1:.3f} | Humidity: r={r2:.3f}, p={p2:.3f}")

# =======================
# 8) Summary stats
# =======================
summary = combined_data[["avg_goals", "avg_attempts", "avg_on_target", "temp", "humidity"]].describe()
print("\n=== Summary ===\n", summary)

# =======================
# 9) Visuals
# =======================
plt.scatter(combined_data["temp"], combined_data["avg_goals"], alpha=0.7)
m, b = np.polyfit(combined_data["temp"], combined_data["avg_goals"], 1)
plt.plot(combined_data["temp"], m*combined_data["temp"]+b, color="red")
plt.title("Average Goals vs Temperature")
plt.xlabel("Temperature (°F)")
plt.ylabel("Average Goals per Match")
plt.show()

plt.scatter(combined_data["humidity"], combined_data["avg_on_target"], alpha=0.7)
m, b = np.polyfit(combined_data["humidity"], combined_data["avg_on_target"], 1)
plt.plot(combined_data["humidity"], m*combined_data["humidity"]+b, color="blue")
plt.title("On-Target Attempts vs Humidity")
plt.xlabel("Humidity (%)")
plt.ylabel("Avg On-Target Attempts")
plt.show()

combined_data.boxplot(column="avg_attempts", by="temp_group", grid=False, patch_artist=True)
plt.title("Attempts by Temperature Group")
plt.xlabel("Temperature Group")
plt.ylabel("Average Attempts per Match")
plt.suptitle("")
plt.show()

# =======================
# 10) Save clean data
# =======================
combined_data.to_csv("cleaned_fifa_weather.csv", index=False)
print("Cleaned dataset saved as 'cleaned_fifa_weather.csv'")

# =======================
# A1) Outliers
# =======================
perf = ["avg_goals", "avg_attempts", "avg_on_target"]
z = np.abs(stats.zscore(combined_data[perf]))
combined_data["is_outlier"] = (z > 3).any(axis=1)
print(f"Outlier matches detected: {combined_data['is_outlier'].sum()}")

# =======================
# A2) Climate Impact Score
# =======================
combined_data["temp_norm"] = (combined_data["temp"] - combined_data["temp"].min()) / (combined_data["temp"].max() - combined_data["temp"].min())
combined_data["humidity_norm"] = (combined_data["humidity"] - combined_data["humidity"].min()) / (combined_data["humidity"].max() - combined_data["humidity"].min())
combined_data["climate_impact_score"] = 0.6 * combined_data["humidity_norm"] + 0.4 * combined_data["temp_norm"]

plt.scatter(combined_data["climate_impact_score"], combined_data["avg_on_target"], alpha=0.7, color="purple")
m, b = np.polyfit(combined_data["climate_impact_score"], combined_data["avg_on_target"], 1)
plt.plot(combined_data["climate_impact_score"], m*combined_data["climate_impact_score"]+b, color="black")
plt.title("Climate Impact Score vs On-Target Attempts")
plt.xlabel("Climate Impact Score (0–1)")
plt.ylabel("Average On-Target Attempts")
plt.show()

combined_data.to_csv("cleaned_fifa_weather_advanced.csv", index=False)
print("Enhanced dataset saved as 'cleaned_fifa_weather_advanced.csv'")
