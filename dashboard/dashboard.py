import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("🚲 Bike Sharing Dashboard")
st.write("Analisis data penyewaan sepeda tahun 2011–2012")

# =========================
# LOAD DATA
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

day_path = BASE_DIR / "data" / "day.csv"
hour_path = BASE_DIR / "data" / "hour.csv"

day_df = pd.read_csv(day_path)
hour_df = pd.read_csv(hour_path)

# =========================
# DATA CLEANING
# =========================

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}

weather_map = {
    1: "Clear",
    2: "Mist",
    3: "Light Snow/Rain",
    4: "Heavy Rain"
}

workingday_map = {
    0: "Holiday",
    1: "Working Day"
}

day_df["season"] = day_df["season"].map(season_map)
day_df["weathersit"] = day_df["weathersit"].map(weather_map)

hour_df["season"] = hour_df["season"].map(season_map)
hour_df["weathersit"] = hour_df["weathersit"].map(weather_map)
hour_df["workingday"] = hour_df["workingday"].map(workingday_map)

# =========================
# SIDEBAR FILTER
# =========================

st.sidebar.header("📌 Filter Dashboard")

selected_season = st.sidebar.selectbox(
    "Pilih Musim",
    options=day_df["season"].unique()
)

filtered_day_df = day_df[
    day_df["season"] == selected_season
]

filtered_hour_df = hour_df[
    hour_df["season"] == selected_season
]

# =========================
# BUSINESS QUESTIONS
# =========================

st.header("📊 Business Questions")

st.markdown("""
### 1. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?

### 2. Pada jam berapa jumlah penyewaan sepeda paling tinggi pada hari kerja dibandingkan hari libur?
""")

# =========================
# SUMMARY METRICS
# =========================

st.header("📈 Summary Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Rental",
        int(filtered_day_df["cnt"].sum())
    )

with col2:
    st.metric(
        "Average Rental",
        round(filtered_day_df["cnt"].mean(), 2)
    )

with col3:
    st.metric(
        "Maximum Rental",
        int(filtered_day_df["cnt"].max())
    )

# =========================
# VISUALIZATION 1
# =========================

st.header("🌤️ Pengaruh Kondisi Cuaca terhadap Rental")

weather_rentals = (
    filtered_day_df
    .groupby("weathersit")["cnt"]
    .mean()
    .reset_index()
)

fig1, ax1 = plt.subplots(figsize=(8, 5))

sns.barplot(
    data=weather_rentals,
    x="weathersit",
    y="cnt",
    ax=ax1
)

ax1.set_title("Rata-rata Rental Berdasarkan Kondisi Cuaca")
ax1.set_xlabel("Kondisi Cuaca")
ax1.set_ylabel("Rata-rata Rental")

st.pyplot(fig1)

st.write("""
### Insight:
- Cuaca cerah menghasilkan jumlah rental tertinggi.
- Semakin buruk cuaca, jumlah rental cenderung menurun.
""")

# =========================
# VISUALIZATION 2
# =========================

st.header("⏰ Pola Rental Berdasarkan Jam")

hourly_rentals = (
    filtered_hour_df
    .groupby(["hr", "workingday"])["cnt"]
    .mean()
    .reset_index()
)

fig2, ax2 = plt.subplots(figsize=(12, 6))

sns.lineplot(
    data=hourly_rentals,
    x="hr",
    y="cnt",
    hue="workingday",
    ax=ax2
)

ax2.set_title("Pola Rental Sepeda Berdasarkan Jam")
ax2.set_xlabel("Jam")
ax2.set_ylabel("Rata-rata Rental")

st.pyplot(fig2)

st.write("""
### Insight:
- Hari kerja memiliki lonjakan rental pada pagi dan sore hari.
- Hari libur memiliki pola rental yang lebih stabil sepanjang hari.
""")

# =========================
# EDA SECTION
# =========================

st.header("🔍 Exploratory Data Analysis")

st.subheader("Statistik Deskriptif")

st.dataframe(filtered_day_df.describe())

# =========================
# RAW DATA
# =========================

st.header("🗂️ Raw Data")

if st.checkbox("Tampilkan Raw Data Day Dataset"):
    st.dataframe(filtered_day_df)

# =========================
# CONCLUSION
# =========================

st.header("✅ Conclusion")

st.markdown("""
### Conclusion 1
Kondisi cuaca memengaruhi jumlah penyewaan sepeda. Cuaca cerah memiliki jumlah rental tertinggi, sedangkan cuaca buruk menyebabkan penurunan jumlah penyewaan.

### Conclusion 2
Pada hari kerja, penyewaan sepeda paling tinggi terjadi pada jam sibuk pagi dan sore hari. Hari libur menunjukkan pola penggunaan yang lebih stabil.

""")

# =========================
# RECOMMENDATION
# =========================

st.header("💡 Recommendation")

st.markdown("""
1. Menambah jumlah sepeda pada jam sibuk hari kerja.
2. Membuat promosi khusus saat cuaca buruk untuk meningkatkan penggunaan.
3. Mengoptimalkan maintenance sepeda pada jam dengan rental rendah.
4. Mengembangkan sistem prediksi rental berdasarkan cuaca dan waktu.
""")