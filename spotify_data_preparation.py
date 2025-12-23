import pandas as pd

def load_spotify_data(file_path: str) -> pd.DataFrame:
    """
    Load Spotify data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file containing Spotify data.

    Returns:
    pd.DataFrame: A DataFrame containing the Spotify data.
    """
    df_high = pd.read_csv('high_popularity_spotify_data.csv')
    df_high['popularity'] = 1
    df_low = pd.read_csv('low_popularity_spotify_data.csv')
    df_low['popularity'] = 0

    df_low = df_low[df_high.columns]
    
    df = pd.concat([df_high, df_low], ignore_index=True)

    return df

def clean_spotify_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Spotify data by handling missing values and removing duplicates.

    Parameters:
    df (pd.DataFrame): The DataFrame containing Spotify data.

    Returns:
    pd.DataFrame: A cleaned DataFrame.
    """
    # Drop rows with any missing values
    df = df.dropna()

    # Drop duplicate rows
    df = df.drop_duplicates()

    # Convert necessary columns to appropriate data types
    df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'],  format='%Y-%m-%d', errors='coerce')

    # Extract year, month, and day from 'track_album_release_date'
    df['release_year'] = df['track_album_release_date'].dt.year
    df['release_month'] = df['track_album_release_date'].dt.month
    df['release_day'] = df['track_album_release_date'].dt.day

    # Dropping columns with no values for the analysis
    no_values_columns = ['track_id', 'track_album_id', 'playlist_id', 'id', 'track_href', 'analysis_url', 'uri', 'type']
    df.drop(columns=no_values_columns, inplace=True)

    # Dealing with missing values from track_album_release_date, release_year, release_month, and release_day
    df['track_album_release_date'] = df['track_album_release_date'].fillna(0)
    df['release_year'] = df['release_year'].fillna(0)
    df['release_month'] = df['release_month'].fillna(0)
    df['release_day'] = df['release_day'].fillna(0)

    return df

def transform_spotify_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the Spotify data by adding new features.

    Parameters:
    df (pd.DataFrame): The DataFrame containing cleaned Spotify data.

    Returns:
    pd.DataFrame: A transformed DataFrame with new features.
    """
    # Convert duration from milliseconds to minutes
    df['duration_minutes'] = df['duration_ms'] / 60000

    # Create a popularity category
    df['popularity_category'] = pd.cut(df['popularity'], 
                                       bins=[-1, 20, 40, 60, 80, 100], 
                                       labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    
    # Convert 'key' and 'mode' to categorical
    df['key'] = df['key'].astype('category')
    df['mode'] = df['mode'].astype('category')

    # Convert release_year, release_month, and release_day to integer
    df.release_year = df.release_year.astype(int)
    df.release_month = df.release_month.astype(int) 
    df.release_day = df.release_day.astype(int) 
    df.time_signature = df.time_signature.astype(int) 

    return df

def prepare_spotify_data(file_path: str) -> pd.DataFrame:
    """
    Load, clean, and transform Spotify data.

    Parameters:
    file_path (str): The path to the CSV file containing Spotify data.

    Returns:
    pd.DataFrame: A prepared DataFrame ready for analysis.
    """
    df = load_spotify_data(file_path)
    df = clean_spotify_data(df)
    df = transform_spotify_data(df)
    return df

if __name__ == "__main__":
    # Example usage
    file_path = 'popularity_spotify_data.csv'
    prepared_data = prepare_spotify_data(file_path)
    print(prepared_data.head())