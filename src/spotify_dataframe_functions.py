import pandas as pd

#A funciton that export the dataframe to a csv file
def export_spotify_data(df: pd.DataFrame, file_path: str) -> None:
    """
    Export the Spotify DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame containing Spotify data.
    file_path (str): The path where the CSV file will be saved.
    """
    df.to_csv(file_path, index=False)
    return

#Funciton that filter the dataframe based on features values
def filter_spotify_data(df: pd.DataFrame, feature: str, threshold) -> pd.DataFrame:
    if df[feature].dtype in [float, int]:
        filtered_df = df[df[feature] >= threshold]
    else:
        filtered_df = df[df[feature] == threshold]

    # print(f"Filtered DataFrame based on {feature} with threshold {threshold}:")
    # print(filtered_df.head())
    return filtered_df


def load_spotify_data(file_path: str) -> pd.DataFrame:
    """
    Load Spotify data from a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file containing Spotify data.

    Returns:
    pd.DataFrame: A DataFrame containing the Spotify data.
    """
    df = pd.read_csv('dataset/' + file_path)

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
    # df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'],  format='%Y-%m-%d', errors='coerce')

    # Extract year, month, and day from 'track_album_release_date'
    # df['release_year'] = df['track_album_release_date'].dt.year
    # df['release_month'] = df['track_album_release_date'].dt.month
    # df['release_day'] = df['track_album_release_date'].dt.day

    # Dropping columns with no values for the analysis
    no_values_columns = ['index']
    df.drop(columns=no_values_columns, inplace=True)

    

    return df

def transform_spotify_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the Spotify data by adding new features.

    Parameters:
    df (pd.DataFrame): The DataFrame containing cleaned Spotify data.

    Returns:
    pd.DataFrame: A transformed DataFrame with new features.
    """

    df.rename(columns={'popularity': 'track_popularity'}, inplace=True)
    df.rename(columns={'artists': 'track_artist'}, inplace=True)


    # Convert duration from milliseconds to minutes
    df['duration_minutes'] = df['duration_ms'] / 60000

    # Create a popularity category
    df['popularity_category'] = pd.cut(df['track_popularity'], 
                                       bins=[-1, 20, 40, 60, 80, 100], 
                                       labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    
    # Convert 'key' and 'mode' to categorical
    df['key'] = df['key'].astype('category')
    df['mode'] = df['mode'].astype('category')

    # Convert release_year, release_month, and release_day to integer
    # df.release_year = df.release_year.astype(int)
    # df.release_month = df.release_month.astype(int) 
    # df.release_day = df.release_day.astype(int) 
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
    file_path = 'dataset_spotify.csv'
    #prepared_data = prepare_spotify_data(file_path)
    #print(prepared_data.head())