# DS 3500: Assignment 3
# Sydney Howard
# NOTE: The datafile was too large to upload to the gradescope. Here is the url for where I found the data
#       if you wish to download it to run the code:
#       https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated/data

import panel as pn
from spotifyapi import SpotifyAPI  # Import  API class

# Loads javascript dependencies and configures Panel (required)
pn.extension()

# Initialize the Spotify API
spotify_api = SpotifyAPI("universal_top_spotify_songs.csv")

# WIDGET DECLARATIONS

# Search Widgets

snapshot_date_select = pn.widgets.DatePicker(name='Select a Snapshot Date', value=spotify_api.df['snapshot_date'].min())

# Plotting Widgets

popularity_slider = pn.widgets.IntSlider(name="Popularity Threshold (Energy vs Danceability)", start=75, end=100, step=5, value=80)
top_artists_dropdown = pn.widgets.IntInput(name="Number of Top Artists (All Data)", value=5, start=1, step=1)
explicit_popularity_dropdown = pn.widgets.IntSlider(name="Popularity Threshold (Explicit vs Nonexplicit)", start=50, end=100, step=5, value=80)

# CALLBACK FUNCTIONS

def get_top_songs_view(date):
    return spotify_api.get_top_10_songs(date)

def get_popularity_vs_danceability_view(date):
    return spotify_api.plot_popularity_vs_danceability(date)

def get_energy_vs_danceability_view(popularity):
    return spotify_api.plot_energy_vs_danceability(popularity)

def get_explicit_vs_nonexplicit_view(threshold):
    return spotify_api.plot_explicit_vs_nonexplicit(threshold)

def get_top_artists_view(count):
    return spotify_api.plot_top_artists(count)

# CALLBACK BINDINGS (Connecting widgets to callback functions)

top_songs_pane = pn.bind(get_top_songs_view, snapshot_date_select)
popularity_vs_danceability_pane = pn.bind(get_popularity_vs_danceability_view, snapshot_date_select)
energy_vs_danceability_pane = pn.bind(get_energy_vs_danceability_view, popularity_slider)
explicit_vs_nonexplicit_pane = pn.bind(get_explicit_vs_nonexplicit_view, explicit_popularity_dropdown)
top_artists_pane = pn.bind(get_top_artists_view, top_artists_dropdown)

# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

# Search card
search_card = pn.Card(
    pn.Column(
        snapshot_date_select,
    ),
    title="Search (Select Date)", width=card_width, collapsed=False
)

# Plots card
plot_card = pn.Card(
    pn.Column(
        popularity_slider,
        explicit_popularity_dropdown,
        top_artists_dropdown
    ),
    title="Plot Settings", width=card_width, collapsed=False
)


# OTHER FEATURES

# Spotify Logo
spotify_logo = pn.pane.PNG("https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg", width=50)

# Description of dash
dashboard_description = pn.pane.Markdown(
    """
    # Spotify Top Songs Dashboard  
    This dashboard provides insights into the top-ranking global Spotify songs over time. The dataset\
    contains daily rankings from 2023-10-18 to 2025-02-10.
    - **Top 10 Songs**: View the highest-ranking tracks for a selected date.  
    - **Popularity vs Danceability**: Examine how song popularity correlates with danceability\
     for the top 10 songs of the selected date.  
    - **Energy vs Danceability**: Analyze how energetic and danceable songs are based on a popularity\
     threshold (all time).  
    - **Explicit vs Non-Explicit Songs**: Compare the presence of explicit tracks at different\
     popularity thresholds (all time).  
    - **Top Artists**: Identify the most frequently appearing artists (all time).  
    """
)

# LAYOUT

layout = pn.template.FastListTemplate(
    title="Spotify Top Songs Dashboard",
    sidebar=[search_card, plot_card],
    theme_toggle=False,
    main=[
        dashboard_description,
        spotify_logo,
        pn.Tabs(
            ("Top 10 Songs (Select Date)", top_songs_pane),
            ("Popularity vs Danceability (Select Date)", popularity_vs_danceability_pane),
            ("Energy vs Danceability (Select Popularity Threshold)", energy_vs_danceability_pane),
            ("Explicit vs Non-Explicit (Select Popularity Threshold)", explicit_vs_nonexplicit_pane),
            ("Top Artists (Select Artist Count)", top_artists_pane),
            active=0
        )
    ],
    header_background='#1ED760'
).servable()

layout.show()