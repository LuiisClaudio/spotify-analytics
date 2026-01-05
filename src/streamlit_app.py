import streamlit as st
import os
import sys

# Ensure local imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import visualization_code
import spotify_dataframe_functions as sdf

st.set_page_config(page_title="The Hit-Science", layout="wide", page_icon="🎵")

color_primary = "#007513"

st._config.set_option('theme.base', 'light')
st._config.set_option('theme.backgroundColor', 'white')
st._config.set_option('theme.secondaryBackgroundColor', '#f0f2f6')
#st._config.set_option('theme.textColor', 'black')
st._config.set_option('theme.primaryColor', '#007513')

# hide_menu_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# header {visibility: hidden;}
# </style>
# """
# st.markdown(hide_menu_style, unsafe_allow_html=True)

# Initialize theme state
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; }
    h1, h2, h3 { color: #007513 !important; font-family: 'Circular', 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 700; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #282828; }
    div[data-testid="metric-container"] { background-color: #282828; border-radius: 10px; padding: 15px; color: #fff; }
</style>
""", unsafe_allow_html=True)

# Load Data
def load_data():
    return sdf.prepare_spotify_data()

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Visualization Render Functions

# Module A
def render_vis_1(df):
    st.subheader("Global Popularity Histogram (Long Tail Analyzer) 📊")

    #genre = st.sidebar.selectbox("Filter by Genre", ["All Genres"] + sorted(df['track_genre'].dropna().unique()))
    #fig = visualization_code.plot_global_popularity_histogram(df, genre)
    fig = visualization_code.plot_global_popularity_histogram(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Show what "normal" vs. "exceptional" popularity looks like for all songs.  
:bar_chart: **Chart Type:** Histogram + KDE.  
 🤔: **Logic:** Most songs are barely heard; only a few are huge hits.  
:secret: **The Hidden Secret:** The music world is a "long tail" tons of obscure tracks, very few superstars.  
:trophy: **Strategic Insight:** See how hard it is to break into the "elite" tier. If the chart has two peaks, it means songs are either hits or totally miss.
""")

def render_vis_2(df):
    st.subheader("The 'Hit Formula' Correlation Matrix 🧪")
    fig = visualization_code.plot_hit_formula_correlation_matrix(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Reveal which audio features actually matter for popularity.  
:art: **Chart Type:** Colorful heatmap.  
 🤔: **Logic:** Shows which features (like loudness, danceability) are linked to hits.  
:secret: **The Hidden Secret:** Vocals are key (instrumental = less popular), and loud songs still win.  
:bulb: **Strategic Insight:** Producers can see what to focus on if "happy" songs are out, the chart will show it!
""")

def render_vis_3(df):
    st.subheader("Genre Market Share vs. Impact Treemap 🗺️")
    fig = visualization_code.plot_genre_market_share_treemap(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Compare genre size vs. average success.  
:triangular_ruler: **Chart Type:** Treemap.  
 🤔: **Logic:** Big rectangles = lots of songs; color = average popularity.  
:secret: **The Hidden Secret:** Some small genres have a higher chance of success per song.  
:blue_heart: **Strategic Insight:** Find "blue ocean" genres less crowded, but fans are super engaged.
""")

def render_vis_4(df):
    st.subheader("Artist Dominance Bubble Swarm 🫧")
    fig = visualization_code.plot_artist_dominance_bubble_swarm(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Show which artists dominate and how.  
:large_blue_circle: **Chart Type:** Bubble swarm.  
 🤔: **Logic:** Bubble size = catalog size; position = popularity.  
:secret: **The Hidden Secret:** Some artists have one big hit, others have lots of songs but less buzz.  
:star2: **Strategic Insight:** Spot "efficient" hitmakers vs. legacy acts who need a comeback.
""")

def render_vis_5(df):
    st.subheader("Explicit Content Popularity Split 🚦")

    # genre = st.sidebar.selectbox("Filter by Genre", ["All Genres"] + sorted(df['track_genre'].dropna().unique()))
    # fig = visualization_code.plot_explicit_content_popularity_split(df, genre)
    fig = visualization_code.plot_explicit_content_popularity_split(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** See if explicit lyrics help or hurt popularity.  
:violin: **Chart Type:** Split violin/box plot.  
 🤔: **Logic:** Compares popularity for explicit vs. clean tracks by genre.  
:secret: **The Hidden Secret:** In some genres, being explicit actually boosts your chances.  
:radio: **Strategic Insight:** Data-driven advice on whether to "clean up" a song or keep it real.
""")

# Module B
def render_vis_6(df):
    st.subheader("The 'Sad Banger' Quadrant (Hexbin Plot) 😢🔥")
    fig = visualization_code.plot_sad_banger_hexbin(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Find the emotional "sweet spot" for hits.  
:hexagon: **Chart Type:** Hexbin plot.  
 🤔: **Logic:** Shows where popular songs cluster in energy vs. mood.  
:secret: **The Hidden Secret:** Modern hits are often high energy but low valence ("sad bangers").  
:fire: **Strategic Insight:** Producers can see exactly which vibe is trending.
""")

def render_vis_7(df):
    st.subheader("The 'Loudness War' Regression 📈🔊")
    fig = visualization_code.plot_loudness_war_regression(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Check if louder songs are still more popular, even with normalization.  
:straight_ruler: **Chart Type:** Scatter + regression line.  
 🤔: **Logic:** Plots loudness vs. popularity, marks Spotify's normalization line.  
:secret: **The Hidden Secret:** Hits are still mastered loud, even if Spotify turns them down.  
:mega: **Strategic Insight:** Don't make your song too quiet listeners still prefer "in your face" sound.
""")

def render_vis_8(df):
    st.subheader("The '30-Second Rule' Duration Decay Curve ⏱️")
    fig = visualization_code.plot_duration_decay_curve(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** See how song length affects popularity.  
:chart_with_upwards_trend: **Chart Type:** Line/area chart.  
 🤔: **Logic:** Shows average popularity by song duration.  
:secret: **The Hidden Secret:** Shorter songs are winning (thanks, TikTok!).  
:scissors: **Strategic Insight:** If short songs do better, cut the filler get to the hook fast.
""")

def render_vis_9(df):
    st.subheader("The Rhythm Profile (Tempo Density) 🥁")
    fig = visualization_code.plot_tempo_density_ridgeline(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Show tempo trends by genre.  
:wave: **Chart Type:** Ridgeline/stacked density.  
 🤔: **Logic:** Plots BPM distributions for each genre.  
:secret: **The Hidden Secret:** "Hit" tempos cluster in certain BPM ranges.  
:runner: **Strategic Insight:** Pick a tempo that fits your genre or break out with a surprise!
""")

def render_vis_10(df):
    st.subheader("Organic vs. Synthetic Density Map 🌱🤖")
    fig = visualization_code.plot_organic_vs_synthetic_density(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Analyze production styles by comparing "Natural" vs. "Processed" sound.  
:fire: **Chart Type:** Density Heatmap.  
 🤔: **Logic:** High **Energy** usually means heavy production (compression, synths), while high **Acousticness** means raw recordings.  
:secret: **The Hidden Secret:** The industry clusters heavily in the "High Energy / Low Acoustic" corner (Hits), but there's a niche for "Raw/Chill" music.  
:control_knobs: **Strategic Insight:** If you want a mainstream hit, you likely need high energy and low acousticness (polished production).
""")

def render_vis_11(df):
    st.subheader("Speechiness Threshold Indicator 🗣️")
    # Allow user to select top N genres
    top_n = st.sidebar.number_input(
        "Number of Top Genres to Show (Speechiness)",
        min_value=1,
        max_value=20,
        value=10,
        step=1,
        help="Select how many top genres (by track count) to display"
    )
    fig = visualization_code.plot_speechiness_threshold_boxplot(df, top_n=top_n)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Warn if a song is too "talky" for playlists.  
:package: **Chart Type:** Boxplot with reference zones.  
 🤔: **Logic:** Shows speechiness by genre, flags risky tracks.  
:secret: **The Hidden Secret:** Too much speechiness = Spotify thinks it's a podcast, not a song.  
:warning: **Strategic Insight:** Avoid high speechiness unless you want to be classified as spoken word.
""")

def render_vis_12(df):
    st.subheader("Sonic Radar (Track Benchmarker) 🕸️")

    # Optimize loading of track list
    # track = st.sidebar.selectbox("Select Track", sorted(df['track_name'].unique())[:1000]) # Limit for performance or use text_input
    # if not track:
    #     track = df['track_name'].iloc[0]
    # fig = visualization_code.plot_sonic_radar(df, track)
    fig = visualization_code.plot_sonic_radar(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Compare your track's audio profile to the global average.  
:spider_web: **Chart Type:** Radar chart.  
 🤔: **Logic:** Overlays your song's features vs. the "hit" average.  
:secret: **The Hidden Secret:** Hits have a balanced "shape" outliers are easy to spot.  
:mag_right: **Strategic Insight:** See exactly where your song stands out or falls short.
""")

# Module C
def render_vis_13(df):
    st.subheader("The 'Camelot Wheel' Key & Mode Heatmap 🎡")
    fig = visualization_code.plot_camelot_wheel_heatmap(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** See which keys and modes are most popular for hits.  
:wheel_of_dharma: **Chart Type:** Sunburst or polar heatmap.  
 🤔: **Logic:** Arranges keys in a circle, shows major/minor and popularity.  
:secret: **The Hidden Secret:** Minor keys are often more popular now, especially for moody genres.  
:musical_keyboard: **Strategic Insight:** If you want a hit, maybe write in C# minor instead of C major!
""")

def render_vis_14(df):
    st.subheader("Genre-Specific Feature Boxplots 📦")
    fig = visualization_code.plot_genre_specific_feature_boxplots(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Compare audio features across genres.  
:bar_chart: **Chart Type:** Boxplots grid.  
 🤔: **Logic:** Shows how things like danceability or energy differ by genre.  
:secret: **The Hidden Secret:** Each genre has its own "normal" outliers can be crossover hits.  
:rocket: **Strategic Insight:** If your song is an outlier for its genre, it might break into new playlists.
""")

def render_vis_15(df):
    st.subheader("Time Signature Stability Gauge ⏲️")
    fig = visualization_code.plot_time_signature_gauge(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Show which time signatures dominate the charts.  
:doughnut: **Chart Type:** Donut chart.  
 🤔: **Logic:** Compares share of 4/4, 3/4, and others.  
:secret: **The Hidden Secret:** Almost all hits are in 4/4 odd meters are super rare.  
:lock: **Strategic Insight:** Unusual time signatures are risky unless you're in a niche genre.
""")

def render_vis_16(df):
    st.subheader("Liveness vs. Popularity Inverse Curve 🎤")
    fig = visualization_code.plot_liveness_vs_popularity(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** See if "live" sounding tracks do well.  
:scatter_plot: **Chart Type:** Scatter with smoothing.  
 🤔: **Logic:** Plots liveness (audience/room sound) vs. popularity.  
:secret: **The Hidden Secret:** Studio-polished tracks usually win; live/raw tracks rarely chart.  
:studio_microphone: **Strategic Insight:** For mass appeal, keep your mix clean and dry.
""")

def render_vis_17(df):
    st.subheader("Explicit Ratio by Genre (Stacked Bar) 🚫")
    fig = visualization_code.plot_explicit_ratio_by_genre(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Show how explicit content varies by genre.  
:bar_chart: **Chart Type:** 100% stacked bar.  
 🤔: **Logic:** Compares explicit vs. clean tracks for each genre.  
:secret: **The Hidden Secret:** Some genres expect explicit lyrics, others don't.  
:scroll: **Strategic Insight:** Match your lyrics to the genre's norms for best results.
""")

def render_vis_18(df):
    st.subheader("The 'Hit Potential' Cluster Map (t-SNE) 🗺️✨")
    st.info("Generating map... simple sampling used for performance.")
    fig = visualization_code.plot_hit_potential_tsne(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Group songs by audio similarity and hit status.  
:crystal_ball: **Chart Type:** t-SNE scatter plot.  
 🤔: **Logic:** Projects all features into 2D, colors by "hit" level.  
:secret: **The Hidden Secret:** "Hit" is its own genre hits from different styles cluster together.  
:compass: **Strategic Insight:** See if your song fits the "hit cluster" or stands out as a niche.
""")

def render_vis_19(df):
    st.subheader("Feature Importance Waterfall Chart 💧")
    fig = visualization_code.plot_feature_importance_waterfall(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Show which features matter most for predicting popularity.  
:chart_with_downwards_trend: **Chart Type:** Waterfall chart.  
 🤔: **Logic:** Ranks features by their impact in a machine learning model.  
:secret: **The Hidden Secret:** Some features (like danceability, loudness) matter way more than others.  
:muscle: **Strategic Insight:** Focus your energy on what actually moves the needle!
""")

def render_vis_20(df):
    st.subheader("The 'Distance to Hit' Gauge 🎯")

    track = st.sidebar.selectbox("Select Track for Hit Distance", sorted(df['track_name'].unique())[:1000])
    if not track:
        track = df['track_name'].iloc[0]
    fig = visualization_code.plot_distance_to_hit_gauge(df, track)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
:dart: **Goal:** Score how close a song is to the "hit" formula.  
:level_slider: **Chart Type:** Gauge/bullet chart.  
 🤔: **Logic:** Compares your track's features to the top 100 hits.  
:secret: **The Hidden Secret:** High score = fits the current hit mold; low score = risky but maybe unique.  
:shield: **Strategic Insight:** Know if your song is "algorithm ready" or a bold outlier.
""")

# Navigation Structure
# --------------------------------------------------------------------------
# STORYTELLING WRAPPERS (Grouping Visualizations for Narrative Flow)
# --------------------------------------------------------------------------

def render_story_market_overview(df):
    st.markdown("### 🌍 Global Market Landscape")
    st.info("Start here to understand the big picture: How strict is the 'Hit' definition, and which genres dominate?")
    render_vis_1(df)
    st.markdown("---")
    render_vis_3(df)

def render_story_artist_strategy(df):
    st.markdown("### 🎤 Artist & Content Strategy")
    st.info("How do artists build catalogs, and how does explicit content affect their reach?")
    render_vis_4(df)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        render_vis_5(df)
    with col2:
        render_vis_17(df)

def render_story_hit_formula(df):
    st.markdown("### 🧪 The 'Hit' Formula")
    st.info("What audio features actually correlate with success? (Data & ML Insights)")
    render_vis_2(df)
    st.markdown("---")
    render_vis_19(df)
    st.markdown("---")
    render_vis_7(df)

def render_story_song_vibes(df):
    st.markdown("### 🎵 Song Architecture & Vibe")
    st.info("Analyzing Emotion, Energy, and Track Duration.")
    render_vis_6(df)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        render_vis_8(df)
    with col2:
        render_vis_16(df)

def render_story_rhythm_texture(df):
    st.markdown("### 🥁 Rhythm & Texture")
    st.info("Tempo, Speechiness, and the Organic/Synthetic balance.")
    render_vis_9(df)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        render_vis_10(df)
    with col2:
        render_vis_11(df)

def render_story_musical_theory(df):
    st.markdown("### 🎼 Musical Theory Deep Dive")
    st.info("Keys, Modes, Time Signatures, and Genre norms.")
    col1, col2 = st.columns(2)
    with col1:
        render_vis_13(df)
    with col2:
        render_vis_15(df)
    st.markdown("---")
    render_vis_14(df)

def render_story_track_analyzer(df):
    st.markdown("### 🎯 Track Analyzer & Prediction")
    st.info("Select a track to benchmark it against Hits and see where it lands on the AI map.")
    col1, col2 = st.columns(2)
    with col1:
        render_vis_12(df)
    with col2:
        render_vis_20(df)
    st.markdown("---")
    render_vis_18(df)

# Navigation Structure
NAV_STRUCTURE = {
    "1. Market Intelligence 📊": {
        "Global Overview": render_story_market_overview,
        "Artist & Strategy": render_story_artist_strategy
    },
    "2. Audio Engineering 🎛️": {
        "The 'Hit' Formula": render_story_hit_formula,
        "Vibe & Architecture": render_story_song_vibes,
        "Rhythm & Texture": render_story_rhythm_texture
    },
    "3. Advanced Insights 🧠": {
        "Musical Theory": render_story_musical_theory,
        "Track Tools (AI)": render_story_track_analyzer
    }
}

# Sidebar Logic
#st.sidebar.markdown("---")
st.sidebar.title("Navigation")
selected_module = st.sidebar.radio("1. Select Module", list(NAV_STRUCTURE.keys()))
selected_app = st.sidebar.radio("2. Select Visualization", list(NAV_STRUCTURE[selected_module].keys()))


# Global Filters
st.sidebar.markdown("---")
st.sidebar.title("Data Filters")

# 0. Popularity Range Filter
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

# 1. Track Genre Filter
if 'track_genre' in df.columns:
    available_genres = sorted(df['track_genre'].dropna().unique())
    selected_genres = st.sidebar.multiselect(
        "Track Genre",
        options=available_genres,
        help="Leave empty to include all genres"
    )

    if selected_genres:
        df = df[df['track_genre'].isin(selected_genres)]

# 2. Select top genre filter, as default is all genres
if 'track_genre' in df.columns:
    top_n_genres = st.sidebar.number_input(
        "Number of Top Genres to Show (Global Filter)",
        min_value=1,
        max_value=len(df['track_genre'].unique()),
        value=len(df['track_genre'].unique()),
        step=1,
        help="Show only the top N genres by track count"
    )
    top_genres = (
        df['track_genre']
        .value_counts()
        .nlargest(top_n_genres)
        .index.tolist()
    )
    df = df[df['track_genre'].isin(top_genres)]

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

# 4. Select top artist filter, as default is all artists
if 'track_artist' in df.columns:
    top_n_artists = st.sidebar.number_input(
        "Number of Top Artists to Show (Global Filter)",
        min_value=1,
        max_value=len(df['track_artist'].unique()),
        value=len(df['track_artist'].unique()),
        step=1,
        help="Show only the top N artists by track count"
    )
    top_artists = (
        df['track_artist']
        .value_counts()
        .nlargest(top_n_artists)
        .index.tolist()
    )
    df = df[df['track_artist'].isin(top_artists)]

#5. Select Track
if 'track_name' in df.columns:
    available_tracks = sorted(df['track_name'].dropna().unique())
    selected_tracks = st.sidebar.multiselect(
        "Track Name",
        options=available_tracks,
        help="Leave empty to include all tracks"
    )

    if selected_tracks:
        df = df[df['track_name'].isin(selected_tracks)]


# Render Application
st.title(selected_module.split(":")[1].strip() if ":" in selected_module else selected_module)
NAV_STRUCTURE[selected_module][selected_app](df)