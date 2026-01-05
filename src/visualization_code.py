import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
from scipy import stats
from sklearn.manifold import TSNE
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler

#1. The Global Popularity Histogram
def plot_global_popularity_histogram(df):
    title_suffix = ""
    chart_df = df

    popularity_data = chart_df['track_popularity']
    
    fig = go.Figure()

    # Histogram
    fig.add_trace(go.Histogram(
        x=popularity_data,
        xbins=dict(start=0, end=100, size=2),
        marker_color='rgba(0, 80, 0, 0.8)',  # dark green
        name='Song Count',
        hovertemplate='Popularity: %{x}<br>Count: %{y}<extra></extra>'
    ))

    # KDE Overlay
    if len(popularity_data) > 1:
        try:
            kde = stats.gaussian_kde(popularity_data)
            x_range = np.linspace(0, 100, 200)
            kde_values = kde(x_range)
            # Scale factor: approximate count to match histogram height
            scale_factor = len(popularity_data) * 2
            scaled_kde = kde_values * scale_factor

            fig.add_trace(go.Scatter(
                x=x_range,
                y=scaled_kde,
                mode='lines',
                name='Trend (KDE)',
                line=dict(color="#72FFA4", width=3, shape='spline'),
                hoverinfo='skip'
            ))
        except Exception:
            pass

    # Reference Zones
    zones = [
        (0, 20, "Long Tail<br>(Obscure)", "rgba(100, 100, 100, 0.1)", "top left"),
        (20, 80, "Mid-Tier<br>(Sustainable)", "rgba(50, 50, 200, 0.05)", "top center"),
        (80, 100, "Elite Tier<br>(Hits)", "rgba(255, 215, 0, 0.1)", "top right")
    ]
    
    # for start, end, label, color, pos in zones:
    #     fig.add_vrect(
    #         x0=start, x1=end,
    #         fillcolor=color, layer="below", line_width=0,
    #         annotation_text=label, annotation_position=pos,
    #         annotation_font_color="rgba(200,200,200,0.7)"
    #     )

    fig.update_layout(
        title=dict(text=f"<b>Global Popularity Distribution</b> {title_suffix}", font=dict(size=20)),
        xaxis_title="Popularity Score (0-100)",
        yaxis_title="Frequency",
        template="plotly_dark",
        bargap=0.1,
        margin=dict(l=40, r=40, t=80, b=40),
        legend=dict(orientation="h", y=1.02, x=1, xanchor="right")
    )
    return fig

#2. The "Hit Formula" Correlation Matrix
def plot_hit_formula_correlation_matrix(df):
    cols = ['track_popularity', 'danceability', 'energy', 'valence', 'loudness', 
            'acousticness', 'instrumentalness', 'speechiness', 'tempo', 'duration_ms']
    
    # Filter only existing columns just in case
    cols = [c for c in cols if c in df.columns]
    
    corr_matrix = df[cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale=[[0, "#FFFFFF"], [1, "#1DB954"]],
        title="<b>The 'Hit Formula' Correlation Matrix</b>"
    )
    fig.update_layout(template="plotly_dark", height=600)
    return fig

#3. Genre Market Share vs. Impact Treemap
def plot_genre_market_share_treemap(df):
    # Aggregating data
    if 'track_genre' not in df.columns:
         return go.Figure().add_annotation(text="No Genre Data", showarrow=False)
         
    genre_stats = df.groupby('track_genre').agg(
        Count=('track_id', 'count'),
        Avg_Pop=('track_popularity', 'mean')
    ).reset_index()
    
    fig = px.treemap(
        genre_stats,
        path=['track_genre'],
        values='Count',
        color='Avg_Pop',
        color_continuous_scale='Viridis',
        title="<b>Genre Market Share vs. Impact</b>",
        hover_data=['Avg_Pop'],
    )
    fig.update_layout(template="plotly_dark", margin=dict(t=50, l=25, r=25, b=25))
    # Note: textinfo might need adjustment based on plotly version
    fig.data[0].textinfo = "label+text+value"
    return fig

#4. Artist Dominance "Bubble Swarm"
def plot_artist_dominance_bubble_swarm(df):
    if 'track_artist' not in df.columns:
        return go.Figure()
        
    # Top 50 artists by track count
    top_artists = df['track_artist'].value_counts().head(50).index
    
    # Mode genre function
    def get_mode_genre(x):
        m = x.mode()
        return m[0] if not m.empty else (x.iloc[0] if len(x) > 0 else "Unknown")
        
    chart_df = df[df['track_artist'].isin(top_artists)].groupby('track_artist').agg(
        Track_Count=('track_id', 'count'),
        Avg_Pop=('track_popularity', 'mean'),
        Primary_Genre=('track_genre', get_mode_genre)
    ).reset_index()
    
    fig = px.scatter(
        chart_df,
        x='Avg_Pop',
        y='Track_Count',
        size='Track_Count',
        color='Primary_Genre',
        hover_name='track_artist',
        size_max=60,
        title="<b>Artist Dominance Bubble Swarm (Top 50)</b>"
    )
    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Average Popularity",
        yaxis_title="Catalog Depth (Track Count)",
        showlegend=False
    )
    return fig

#5. The Explicit Content Popularity Split
def plot_explicit_content_popularity_split(df, selected_genre=None):
    # if selected_genre and selected_genre != "All Genres":
    #     chart_df = df[df['track_genre'] == selected_genre]
    # else:
    #     # Use top 10 genres to keep it readable
    #     top_genres = df['track_genre'].value_counts().head(10).index
    #     chart_df = df[df['track_genre'].isin(top_genres)]

    chart_df = df

    fig = px.box(
        chart_df,
        x='track_genre',
        y='track_popularity',
        color='explicit',
        title="<b>Explicit Content Popularity Split</b>",
        color_discrete_map={True: '#FF5555', False: "#03B300"}
    )
    fig.update_layout(template="plotly_dark", xaxis_title="Genre", yaxis_title="track_popularity")
    return fig

#6. The "Sad Banger" Quadrant (Hexbin Plot)
def plot_sad_banger_hexbin(df):
    fig = px.density_heatmap(
        df,
        x="valence",
        y="energy",
        z="track_popularity",
        histfunc="avg",
        nbinsx=20,
        nbinsy=20,
        color_continuous_scale="Greens",
        title="<b>The 'Sad Banger' Quadrant</b> (Avg Popularity)"
    )
    
    # Quadrant Labels
    fig.add_annotation(x=0.9, y=0.9, text="Happy/Energetic", showarrow=False, font=dict(color="white"))
    fig.add_annotation(x=0.1, y=0.9, text="Angry/Turbulent", showarrow=False, font=dict(color="white"))
    fig.add_annotation(x=0.1, y=0.1, text="Sad/Depressing", showarrow=False, font=dict(color="white"))
    fig.add_annotation(x=0.9, y=0.1, text="Chill/Peaceful", showarrow=False, font=dict(color="white"))
    
    fig.update_layout(template="plotly_dark", xaxis_title="Valence (Positivity)", yaxis_title="Energy")
    return fig

#7. The "Loudness War" Regression
def plot_loudness_war_regression(df):
    chart_df = df.sample(5000) if len(df) > 5000 else df
    
    fig = px.scatter(
        chart_df,
        x="loudness",
        y="track_popularity",
        trendline="lowess",
        trendline_color_override="#1DB954",
        opacity=0.3,
        title="<b>The 'Loudness War' Regression</b>"
    )
    
    fig.add_vline(x=-14, line_width=2, line_dash="dash", line_color="red", annotation_text="Spotify Norm (-14dB)")
    fig.update_layout(template="plotly_dark", xaxis_title="Loudness (dB)", yaxis_title="track_popularity")
    return fig

#8. The "30-Second Rule" Duration Decay Curve
def plot_duration_decay_curve(df):
    # Avoid SettingWithCopy
    df_c = df.copy()
    df_c['duration_sec'] = df_c['duration_ms'] / 1000
    df_c['duration_bin'] = (df_c['duration_sec'] // 15) * 15 
    
    agg_df = df_c.groupby('duration_bin')['track_popularity'].mean().reset_index()
    agg_df = agg_df[agg_df['duration_bin'] < 600] 
    
    fig = px.area(
        agg_df,
        x='duration_bin',
        y='track_popularity',
        title="<b>Duration Decay Curve</b>",
        line_shape='spline'
    )
    fig.update_traces(line_color='#1DB954', fillcolor='rgba(29, 185, 84, 0.2)')
    fig.update_layout(template="plotly_dark", xaxis_title="Duration (Seconds)", yaxis_title="Average Popularity")
    return fig

#9. The Rhythm Profile (Tempo Density)
def plot_tempo_density_ridgeline(df, top_n=10):
    # top_genres = df['track_genre'].value_counts().head(top_n).index
    # chart_df = df[df['track_genre'].isin(top_genres)]

    chart_df = df
    
    fig = px.violin(
        chart_df,
        y="track_genre",
        x="tempo",
        color="track_genre",
        orientation="h",
        #side="positive",
        points=False, # cleaner look
        title="<b>The Rhythm Profile (Tempo)</b>"
    )
    fig.update_layout(template="plotly_dark", showlegend=False, xaxis_title="BPM")
    return fig

#10. "Organic vs. Synthetic" Density Map
def plot_organic_vs_synthetic_density(df):
    fig = px.density_heatmap(
        df,
        x="acousticness",
        y="energy",
        nbinsx=20,
        nbinsy=20,
        color_continuous_scale="Inferno",
        title="<b>Production Style: Acoustic vs. Energy</b>",
        labels={"acousticness": "Acousticness (Natural/Raw)", "energy": "Energy (Processed/Intense)"}
    )
    
    # Add quadrant annotations for context
    fig.add_annotation(x=0.1, y=0.9, text="<b>Modern Pop/Electronic</b><br>(Processed & Loud)", showarrow=False, font=dict(color="white", size=10))
    fig.add_annotation(x=0.9, y=0.1, text="<b>Acoustic/Folk</b><br>(Natural & Dynamic)", showarrow=False, font=dict(color="white", size=10))
    
    fig.update_layout(
        template="plotly_dark",
        margin=dict(t=50, l=20, r=20, b=20)
    )
    return fig

#11. Speechiness Threshold Indicator
def plot_speechiness_threshold_boxplot(df, top_n=10):
    top_genres = df['track_genre'].value_counts().head(top_n).index
    chart_df = df[df['track_genre'].isin(top_genres)]
    
    fig = px.box(
        chart_df,
        x="track_genre",
        y="speechiness",
        color="track_genre",
        title="<b>Speechiness Threshold Indicator</b>",
        color_discrete_sequence=px.colors.sequential.Greens
    )
    
    fig.add_hrect(y0=0.66, y1=1.0, fillcolor="blue", opacity=0.5, layer="below", annotation_text="Spoken Word")
    fig.add_hrect(y0=0.33, y1=0.66, fillcolor="blue", opacity=0.4, layer="below", annotation_text="Rap/Rhythmic")
    fig.add_hrect(y0=0.0, y1=0.33, fillcolor="blue", opacity=0.3, layer="below", annotation_text="Music")
    
    fig.update_layout(template="plotly_dark", xaxis_title="Genre", yaxis_title="Speechiness")
    return fig

#12. Sonic Radar
def plot_sonic_radar(df):
    
    #if df has only one row change track_name to the track name of that row
    if len(df) == 1:
        track_name = df['track_name'].iloc[0]
    else:
        track_name = 'Agg values'
    
    features = ['danceability', 'energy', 'valence', 'acousticness', 'liveness', 'speechiness']
    
    track_data = df
    
    if track_data.empty:
        fig = go.Figure()
        fig.add_annotation(text="Track not found", showarrow=False, font_size=20)
        fig.update_layout(template="plotly_dark")
        return fig
        
    track_vals = track_data[features].values.flatten().tolist()
    # Close the polygon
    track_vals += [track_vals[0]]
    
    avg_vals = df[features].mean().values.flatten().tolist()
    avg_vals += [avg_vals[0]]
    
    categories = features + [features[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=avg_vals,
        theta=categories,
        fill='toself',
        name='Global Average',
        line_color='gray',
        opacity=0.5
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=track_vals,
        theta=categories,
        fill='toself',
        name=str(track_name)[:20], # Truncate if long
        line_color='#1DB954'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        template="plotly_dark",
        title=f"<b>Sonic Radar: {track_name}</b>"
    )
    return fig

#13. Camelot Wheel Heatmap
def plot_camelot_wheel_heatmap(df):
    key_mapping = {
        0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F', 
        6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'
    }
    df_c = df.copy()
    df_c['key_name'] = df_c['key'].map(key_mapping)
    df_c['mode_name'] = df_c['mode'].map({1: 'Major', 0: 'Minor'})
    
    grouped = df_c.groupby(['mode_name', 'key_name'])['track_popularity'].mean().reset_index()
    
    fig = px.sunburst(
        grouped,
        path=['mode_name', 'key_name'],
        values='track_popularity',
        color='track_popularity',
        color_continuous_scale='Greens',
        title="<b>Key & Mode Popularity Heatmap</b>"
    )
    fig.update_layout(template="plotly_dark")
    return fig

#14. Genre Feature Boxplots
def plot_genre_specific_feature_boxplots(df):
    top_genres = df['track_genre'].value_counts().head(5).index
    chart_df = df[df['track_genre'].isin(top_genres)]
    
    melted = chart_df.melt(id_vars=['track_genre'], value_vars=['danceability', 'energy', 'valence', 'acousticness'])
    
    fig = px.box(
        melted,
        x="track_genre",
        y="value",
        color="track_genre",
        facet_col="variable",
        title="<b>Genre-Specific Feature Distribution</b>",
        color_discrete_sequence=["#1DB954"]  # Spotify green
        #color_discrete_sequence=px.colors.sequential.Greens  # Spectrum of green
    )
    fig.update_layout(template="plotly_dark", showlegend=False)
    return fig

#15. Time Signature Gauge
def plot_time_signature_gauge(df):
    counts = df['time_signature'].value_counts(normalize=True).reset_index()
    counts.columns = ['Signature', 'Percentage']
    
    fig = px.treemap(
        counts,
        path=['Signature'],
        values='Percentage',
        title="<b>Time Signature Stability</b>",
        color='Percentage',
        color_continuous_scale='Greens'
    )
    fig.update_layout(template="plotly_dark")
    return fig

#16. Liveness vs. Popularity
def plot_liveness_vs_popularity(df):
    chart_df = df.sample(2000) if len(df) > 2000 else df
    
    fig = px.scatter(
        chart_df,
        x="liveness",
        y="track_popularity",
        trendline="lowess",
        trendline_color_override="Black",
        opacity=0.4,
        title="<b>Liveness vs. Popularity</b>",
        color_discrete_sequence=["#1DB954"]  # Spotify green
    )
    fig.update_layout(template="plotly_dark")
    return fig

#17. Explicit Ratio by Genre
def plot_explicit_ratio_by_genre(df):
    top_genres = df['track_genre'].value_counts().head(20).index
    chart_df = df[df['track_genre'].isin(top_genres)]
    
    grouped = chart_df.groupby(['track_genre', 'explicit']).size().reset_index(name='count')
    # Normalize to 100% stack
    totals = grouped.groupby('track_genre')['count'].transform('sum')
    grouped['percentage'] = grouped['count'] / totals
    
    fig = px.bar(
        grouped,
        x="track_genre",
        y="percentage",
        color="explicit",
        title="<b>Explicit Content Ratio by Genre</b>",
        color_discrete_map={True: "#B5FFCF", False: '#1DB954'}
    )
    fig.update_layout(template="plotly_dark", xaxis_tickangle=-45, yaxis_tickformat=".0%")
    return fig

#18. t-SNE
def plot_hit_potential_tsne(df):
    sample_size = 500
    if len(df) > sample_size:
        chart_df = df.sample(sample_size, random_state=42).copy()
    else:
        chart_df = df.copy()

    features = ['danceability', 'energy', 'valence', 'acousticness', 'loudness', 'tempo']
    # Handle missing
    X = chart_df[features].fillna(0)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    tsne = TSNE(n_components=2, random_state=42, perplexity=30)
    projections = tsne.fit_transform(X_scaled)
    
    chart_df['tsne_1'] = projections[:, 0]
    chart_df['tsne_2'] = projections[:, 1]
    
    chart_df['Pop_Tier'] = pd.cut(chart_df['track_popularity'], bins=[-1, 30, 70, 100], labels=['Niche', 'Mid', 'Hit'])
    
    fig = px.scatter(
        chart_df,
        x='tsne_1',
        y='tsne_2',
        color='Pop_Tier',
        hover_data=['track_name', 'track_artist'],
        title="<b>'Hit Potential' Audio Landscape (t-SNE)</b>",
        color_discrete_map={'Hit': '#1DB954', 'Mid': "#FFA024", 'Niche': 'gray'}
    )
    fig.update_layout(template="plotly_dark", xaxis_visible=False, yaxis_visible=False)
    return fig

#19. Feature Importance
def plot_feature_importance_waterfall(df):
    features = ['danceability', 'energy', 'valence', 'loudness', 'acousticness', 'instrumentalness', 'speechiness', 'tempo', 'duration_ms', 'liveness']
    chart_df = df.dropna(subset=features + ['track_popularity']).sample(min(1000, len(df)))
    
    X = chart_df[features]
    y = chart_df['track_popularity']
    
    model = RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42)
    model.fit(X, y)
    
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)
    
    fig = go.Figure(go.Waterfall(
        name = "Importance", orientation = "h",
        measure = ["relative"] * len(features),
        y = [features[i] for i in sorted_idx],
        x = [importances[i] for i in sorted_idx],
        connector = {"mode":"between", "line":{"width":4, "color":"rgb(0, 0, 0)", "dash":"solid"}}
    ))

    fig.update_layout(
        title = "<b>Feature Importance for Popularity</b>",
        template="plotly_dark"
    )
    return fig

#20. Distance to Hit Gauge
def plot_distance_to_hit_gauge(df, track_name):
    hits = df[df['track_popularity'] > 75]
    if hits.empty:
         hits = df[df['track_popularity'] > 60] 
         
    features = ['danceability', 'energy', 'valence', 'acousticness', 'loudness']
    
    if hits.empty:
        return go.Figure().add_annotation(text="Not enough hits data")
        
    hit_centroid = hits[features].mean()
    
    target = df[df['track_name'] == track_name]
    if target.empty:
        return go.Figure().add_annotation(text="Track not found")

    target_vals = target[features].iloc[0]
    
    # Scale for distance calc
    scaler = MinMaxScaler()
    # Fit on all + specific track to cover range
    combined = pd.concat([hits[features], target[features]])
    scaler.fit(combined)
    
    centroid_scaled = scaler.transform([hit_centroid])[0]
    target_scaled = scaler.transform([target_vals])[0]
    
    dist = np.linalg.norm(centroid_scaled - target_scaled)
    # Max possible Euclidean dist in 5D hypercube is sqrt(5) ~= 2.236
    max_dist = np.sqrt(len(features))
    score = max(0, 100 * (1 - (dist / max_dist))) 
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "Hit Similarity Score"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#1DB954"},
            'steps' : [
                {'range': [0, 50], 'color': "#006925"},
                {'range': [50, 80], 'color': "#D9FFE6"},
                {'range': [80, 100], 'color': "white"}
            ],
            'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}
        }
    ))
    fig.update_layout(template="plotly_dark")
    return fig
