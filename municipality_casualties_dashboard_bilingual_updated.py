
import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
@st.cache_data
def load_data():
    return pd.read_excel("total_casualties_by_municipality_cleaned.xlsx")

df = load_data()

# Sidebar language toggle
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
        "en": "Map View (Municipalities with coordinates only)",
        "he": "תצוגת מפה (רק רשויות עם קואורדינטות יוצגו)"
    }
}

# Title and filters
st.title(lang_dict["title"][lang])
metric = st.sidebar.selectbox(lang_dict["metric_select"][lang], ["Total Casualties", "Total Deaths", "Currently Hospitalized"])
top_n = st.sidebar.slider(lang_dict["top_n_select"][lang], 5, 20, 10)

# Filter top N
top_data = df.sort_values(by=metric, ascending=False).head(top_n)

# Bar chart
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

# Map view
st.markdown(f"### {lang_dict['map_title'][lang]}")
df_map = df.dropna(subset=["Latitude", "Longitude"])
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
