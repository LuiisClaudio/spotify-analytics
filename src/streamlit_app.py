import streamlit as st
import os
import sys

# Ensure local imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import visualization_code
import spotify_dataframe_functions as sdf

st.set_page_config(page_title="The Hit-Science Intelligence Suite", layout="wide", page_icon="🎵")

color_primary = "#1DB954"

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #1DB954; }
    h1, h2, h3 { color: #1DB954 !important; font-family: 'Circular', 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 700; }
    [data-testid="stSidebar"] { background-color: #B8DCC5; border-right: 1px solid #282828; }
    div[data-testid="metric-container"] { background-color: #282828; border-radius: 10px; padding: 15px; color: #fff; }
</style>
""", unsafe_allow_html=True)

# Load Data
def load_data():
    return sdf.prepare_spotify_data('dataset_spotify.csv')

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Visualization Render Functions

# Module A
def render_vis_1(df):
    st.subheader("1. Global Popularity Histogram (Long Tail Analyzer)")
    st.sidebar.markdown("---")
    #genre = st.sidebar.selectbox("Filter by Genre", ["All Genres"] + sorted(df['track_genre'].dropna().unique()))
    #fig = visualization_code.plot_global_popularity_histogram(df, genre)
    fig = visualization_code.plot_global_popularity_histogram(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_2(df):
    st.subheader("2. The 'Hit Formula' Correlation Matrix")
    fig = visualization_code.plot_hit_formula_correlation_matrix(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_3(df):
    st.subheader("3. Genre Market Share vs. Impact Treemap")
    fig = visualization_code.plot_genre_market_share_treemap(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_4(df):
    st.subheader("4. Artist Dominance Bubble Swarm")
    fig = visualization_code.plot_artist_dominance_bubble_swarm(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_5(df):
    st.subheader("5. Explicit Content Popularity Split")
    st.sidebar.markdown("---")
    genre = st.sidebar.selectbox("Filter by Genre", ["All Genres"] + sorted(df['track_genre'].dropna().unique()))
    fig = visualization_code.plot_explicit_content_popularity_split(df, genre)
    st.plotly_chart(fig, use_container_width=True)

# Module B
def render_vis_6(df):
    st.subheader("6. The 'Sad Banger' Quadrant (Hexbin Plot)")
    fig = visualization_code.plot_sad_banger_hexbin(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_7(df):
    st.subheader("7. The 'Loudness War' Regression")
    fig = visualization_code.plot_loudness_war_regression(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_8(df):
    st.subheader("8. The '30-Second Rule' Duration Decay Curve")
    fig = visualization_code.plot_duration_decay_curve(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_9(df):
    st.subheader("9. The Rhythm Profile (Tempo Density)")
    fig = visualization_code.plot_tempo_density_ridgeline(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_10(df):
    st.subheader("10. Organic vs. Synthetic Density Map")
    fig = visualization_code.plot_organic_vs_synthetic_density(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_11(df):
    st.subheader("11. Speechiness Threshold Indicator")
    fig = visualization_code.plot_speechiness_threshold_boxplot(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_12(df):
    st.subheader("12. Sonic Radar (Track Benchmarker)")
    st.sidebar.markdown("---")
    # Optimize loading of track list
    track = st.sidebar.selectbox("Select Track", sorted(df['track_name'].unique())[:1000]) # Limit for performance or use text_input
    if not track:
        track = df['track_name'].iloc[0]
    fig = visualization_code.plot_sonic_radar(df, track)
    st.plotly_chart(fig, use_container_width=True)

# Module C
def render_vis_13(df):
    st.subheader("13. The 'Camelot Wheel' Key & Mode Heatmap")
    fig = visualization_code.plot_camelot_wheel_heatmap(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_14(df):
    st.subheader("14. Genre-Specific Feature Boxplots")
    fig = visualization_code.plot_genre_specific_feature_boxplots(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_15(df):
    st.subheader("15. Time Signature Stability Gauge")
    fig = visualization_code.plot_time_signature_gauge(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_16(df):
    st.subheader("16. Liveness vs. Popularity Inverse Curve")
    fig = visualization_code.plot_liveness_vs_popularity(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_17(df):
    st.subheader("17. Explicit Ratio by Genre (Stacked Bar)")
    fig = visualization_code.plot_explicit_ratio_by_genre(df)
    st.plotly_chart(fig, use_container_width=True)

# Module D
def render_vis_18(df):
    st.subheader("18. The 'Hit Potential' Cluster Map (t-SNE)")
    st.info("Generating map... simple sampling used for performance.")
    fig = visualization_code.plot_hit_potential_tsne(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_19(df):
    st.subheader("19. Feature Importance Waterfall Chart")
    fig = visualization_code.plot_feature_importance_waterfall(df)
    st.plotly_chart(fig, use_container_width=True)

def render_vis_20(df):
    st.subheader("20. The 'Distance to Hit' Gauge")
    st.sidebar.markdown("---")
    track = st.sidebar.selectbox("Select Track for Hit Distance", sorted(df['track_name'].unique())[:1000])
    if not track:
        track = df['track_name'].iloc[0]
    fig = visualization_code.plot_distance_to_hit_gauge(df, track)
    st.plotly_chart(fig, use_container_width=True)


# Navigation Structure
NAV_STRUCTURE = {
    "A: Macro-Market Intelligence": {
        "1. Global Popularity Histogram": render_vis_1,
        "2. Hit Formula Matrix": render_vis_2,
        "3. Market Share Treemap": render_vis_3,
        "4. Artist Bubble Swarm": render_vis_4,
        "5. Explicit Content Split": render_vis_5
    },
    "B: Sonic DNA (Engineering a Hit)": {
        "6. Sad Banger Hexbin": render_vis_6,
        "7. Loudness War Regression": render_vis_7,
        "8. Duration Decay Curve": render_vis_8,
        "9. Rhythm Profile": render_vis_9,
        "10. Organic vs Synthetic": render_vis_10,
        "11. Speechiness Threshold": render_vis_11,
        "12. Sonic Radar": render_vis_12
    },
    "C: Genre & Cultural Context": {
        "13. Camelot Wheel Heatmap": render_vis_13,
        "14. Feature Boxplots": render_vis_14,
        "15. Time Sig. Stability": render_vis_15,
        "16. Liveness vs Popularity": render_vis_16,
        "17. Explicit Ratio": render_vis_17
    },
    "D: Secret Sauce (Advanced Analytics)": {
        "18. Hit Potential t-SNE": render_vis_18,
        "19. Feature Importance": render_vis_19,
        "20. Distance to Hit Gauge": render_vis_20
    }
}

    

# Global Filters
st.sidebar.markdown("---")
st.sidebar.title("Data Filters")

# 1. Popularity Range Filter
if 'track_popularity' in df.columns:
    min_pop = int(df['track_popularity'].min())
    max_pop = int(df['track_popularity'].max())
    
    popularity_range = st.sidebar.slider(
        "Popularity Range",
        min_value=min_pop,
        max_value=max_pop,
        value=(min_pop, max_pop)
    )
    df = df[(df['track_popularity'] >= popularity_range[0]) & (df['track_popularity'] <= popularity_range[1])]

# 2. Track Genre Filter
if 'track_genre' in df.columns:
    available_genres = sorted(df['track_genre'].dropna().unique())
    selected_genres = st.sidebar.multiselect(
        "Track Genre",
        options=available_genres,
        help="Leave empty to include all genres"
    )

    if selected_genres:
        df = df[df['track_genre'].isin(selected_genres)]

#3. Artist Filter
if 'track_artist' in df.columns:
    available_artists = sorted(df['track_artist'].dropna().unique())
    selected_artists = st.sidebar.multiselect(
        "Artist Name",
        options=available_artists,
        help="Leave empty to include all artists"
    )

    if selected_artists:
        df = df[df['track_artist'].isin(selected_artists)]

# Sidebar Logic
st.sidebar.markdown("---")
st.sidebar.title("Navigation")
selected_module = st.sidebar.selectbox("1. Select Module", list(NAV_STRUCTURE.keys()))
selected_app = st.sidebar.radio("2. Select Application", list(NAV_STRUCTURE[selected_module].keys()))

# Render Application
st.title(selected_module.split(":")[1].strip() if ":" in selected_module else selected_module)
NAV_STRUCTURE[selected_module][selected_app](df)