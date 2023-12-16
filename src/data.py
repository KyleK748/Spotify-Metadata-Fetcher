import pandas as pd
import numpy as np
import json
from main import get_token, search_for_artist, get_all_songs_metadata_by_artist

# Get valid token
token = get_token()
# Search for artist, 
result = search_for_artist(token, "The Beatles")
artist_id = result['id']
# Get metadata for all songs of artist
all_songs_metadata = get_all_songs_metadata_by_artist(token, artist_id)

# Convert to DataFrame
df = pd.DataFrame(all_songs_metadata)

# Format DataFrame, drop unnecessary columns, transform ms to min:sec
df['ISRC'] = df['external_ids'].apply(lambda x: x['isrc'])
df['duration'] = df['duration_ms'].apply(lambda x: f"{x // 60000}:{(x % 60000) // 1000:02}")
df = df.drop(columns=['duration_ms', 'external_ids'], axis=1)

# Print first 5 rows of DataFrame
print(df.head())

# Save DataFrame to Excel
df.to_excel('', index=False)
