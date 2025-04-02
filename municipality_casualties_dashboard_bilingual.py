
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("total_casualties_by_municipality.xlsx")

df = load_data()

# Convert numeric columns
df["Total Casualties"] = pd.to_numeric(df["Total Casualties"], errors="coerce")
df["Total Deaths"] = pd.to_numeric(df["Total Deaths"], errors="coerce")
df["Currently Hospitalized"] = pd.to_numeric(df["Currently Hospitalized"], errors="coerce")

# Language toggle
language = st.sidebar.radio("Language / שפה", ["English", "עברית"])
lang = "en" if language == "English" else "he"

# Language dictionary
lang_dict = {
    "title": {
        "en": "Municipality Casualties Dashboard",
        "he": "לוח בקרה - נפגעים לפי רשות"
    },
    "metric_select": {
        "en": "Choose metric to visualize:",
        "he": "בחר מדד להצגה:"
    },
    "top_n_select": {
        "en": "Select number of municipalities to display:",
        "he": "בחר מספר רשויות לתצוגה:"
    },
    "map_title": {
        "en": "Map View (Municipalities without coordinates not shown)",
        "he": "מפת רשויות (ללא קואורדינטות לא יוצגו)"
    }
}

# Page title
st.title(lang_dict["title"][lang])

# Sidebar options
metric = st.sidebar.selectbox(
    lang_dict["metric_select"][lang],
    ["Total Casualties", "Total Deaths", "Currently Hospitalized"]
)
top_n = st.sidebar.slider(lang_dict["top_n_select"][lang], 5, 20, 10)

# Filter top N
top_data = df.sort_values(by=metric, ascending=False).head(top_n)

# Bar Chart
fig_bar = px.bar(
    top_data,
    x="Municipality",
    y=metric,
    color="Municipality",
    text_auto=True,
    title=f"{metric} - Top {top_n}"
)
fig_bar.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_bar)

# Optional: Add coordinates manually for a few known municipalities for demo
coords = {
    "אשקלון": (31.6693, 34.5715),
    "תל אביב - יפו": (32.0853, 34.7818),
    "ירושלים": (31.7683, 35.2137),
    "שדרות": (31.5208, 34.5964),
    "עוטף עזה": (31.4, 34.5)
}
df["Latitude"] = df["Municipality"].map(lambda x: coords.get(x, (None, None))[0])
df["Longitude"] = df["Municipality"].map(lambda x: coords.get(x, (None, None))[1])
df_map = df.dropna(subset=["Latitude", "Longitude"])

# Map
st.markdown(f"### {lang_dict['map_title'][lang]}")
fig_map = px.scatter_mapbox(
    df_map,
    lat="Latitude",
    lon="Longitude",
    size=metric,
    color="Municipality",
    hover_name="Municipality",
    size_max=40,
    zoom=7,
    mapbox_style="carto-positron"
)
st.plotly_chart(fig_map)
