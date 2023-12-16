# Spotify Metadata Fetcher

This project allows you to fetch metadata for all songs of a specific artist from the Spotify API in bulk. It's a great tool if you need to get ISRC and duration data for multiple tracks at once.

## Setup

1. Register an account at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create a new application.

2. After creating the application, you'll be provided with a `Client ID` and `Client Secret`. 

3. Create a `.env` file in the root directory of this project and add your `Client ID` and `Client Secret` as follows:

    ```
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```

## Usage

1. Open `data.py` and specify the name of the artist you want to fetch data for.

2. Run `data.py`. This will fetch the metadata and save it as a DataFrame.

3. The DataFrame is then saved to an Excel file. You can modify the code to change the output format or manipulate the data further.

## Note

Please ensure that you have the necessary permissions to use the Spotify API and the data you fetch.
