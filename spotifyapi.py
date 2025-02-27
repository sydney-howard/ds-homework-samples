# DS 3500: Assignment 3
# Sydney Howard

import pandas as pd
import plotly.express as px
import panel as pn

class SpotifyAPI:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.clean_data()

    def clean_data(self):
        """Cleans the dataset by converting types and handling missing values.
        Also eliminates the country column to focus on global trends."""
        self.df['snapshot_date'] = pd.to_datetime(self.df['snapshot_date'])
        self.df['popularity'] = pd.to_numeric(self.df['popularity'], errors='coerce')
        self.df['daily_rank'] = pd.to_numeric(self.df['daily_rank'], errors='coerce')
        self.df = self.df.dropna(
            subset=['popularity', 'danceability', 'energy', 'daily_rank', 'snapshot_date', 'name', 'artists',
                    'is_explicit'])
        self.df = self.df[self.df['country'].isnull()].drop(columns=['country'])
        self.df['is_explicit'] = self.df['is_explicit'].astype(bool)
        self.df['popularity'] = pd.to_numeric(self.df['popularity'], downcast='integer')
        self.df['daily_rank'] = pd.to_numeric(self.df['daily_rank'], downcast='integer')

    def get_top_10_songs(self, snapshot_date):
        """Return the top 10 songs for a given snapshot date."""
        snapshot_date = pd.to_datetime(snapshot_date).normalize()
        filtered_df = self.df[self.df['snapshot_date'].dt.normalize() == snapshot_date].nsmallest(10, 'daily_rank')

        if filtered_df.empty:
            return pn.pane.Markdown(f"### Top 10 Songs on {snapshot_date.date()}\nNo data available.")

        table = filtered_df[['daily_rank', 'name', 'artists']].rename(columns={
            'daily_rank': 'Rank', 'name': 'Song Name', 'artists': 'Artist(s)'
        }).reset_index(drop=True)

        return pn.widgets.DataFrame(table, disabled=True, width=600, show_index=False)

    def plot_popularity_vs_danceability(self, snapshot_date):
        """Generate a scatter plot of popularity vs danceability
        for the top 10 songs of a given date."""
        snapshot_date = pd.to_datetime(snapshot_date).normalize()
        filtered_df = self.df[self.df['snapshot_date'].dt.normalize() == snapshot_date].nsmallest(10, 'daily_rank')

        if filtered_df.empty:
            return pn.pane.Markdown("No data available for the selected date.")

        # Plot
        fig = px.scatter(filtered_df, x='danceability', y='popularity', size='popularity', hover_name='name',
                         title=f'Top 10 Songs: Popularity vs Danceability on {snapshot_date.date()}')
        return pn.pane.Plotly(fig)

    def plot_energy_vs_danceability(self, popularity_filter):
        """Generate a scatter plot of energy vs danceability
        for songs above a given popularity threshold."""
        filtered_df = self.df[self.df['popularity'] >= popularity_filter]
        if filtered_df.empty:
            return pn.pane.Markdown("No data available for the selected filter.")

        # Plot
        fig = px.scatter(filtered_df, x='danceability', y='energy', size='popularity', hover_name='name',
                         title=f'Energy vs Danceability (Popularity ≥ {popularity_filter}) - All Data')
        return pn.pane.Plotly(fig)

    def plot_explicit_vs_nonexplicit(self, popularity_threshold):
        """Generate a bar chart comparing explicit and non-explicit
        song counts above a popularity threshold."""
        filtered_df = self.df[self.df['popularity'] >= popularity_threshold]
        if filtered_df.empty:
            return pn.pane.Markdown("No data available for the selected popularity threshold.")

        explicit_counts = filtered_df['is_explicit'].value_counts()
        labels = ["Non-Explicit" if val is False else "Explicit" for val in explicit_counts.index]
        values = explicit_counts.values

        # Plot
        fig = px.bar(x=labels, y=values, labels={'x': 'Explicit Content', 'y': 'Song Count'},
                     title=f'Explicit vs Non-Explicit Songs (Popularity ≥ {popularity_threshold}) - All Data')
        return pn.pane.Plotly(fig)

    def plot_top_artists(self, n_top_artists):
        """Generate a bar chart of the top N most frequently appearing artists."""
        artist_counts = self.df['artists'].value_counts().nlargest(n_top_artists)
        if artist_counts.empty:
            return pn.pane.Markdown("No data available for the selected number of artists.")

        # Plot
        fig = px.bar(x=artist_counts.index, y=artist_counts.values,
                     labels={'x': 'Artist', 'y': 'Song Appearances'},
                     title=f'Top {n_top_artists} Most Frequent Artists - All Data')
        return pn.pane.Plotly(fig)
