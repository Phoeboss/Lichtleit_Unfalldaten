import pandas as pd
from pyproj import Proj, transform
import sys
import utm
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from sklearn.cluster import DBSCAN
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from sklearn.cluster import DBSCAN


############################################
# Function to filter data
# This is the function where you can add code to filter the dataframe as needed
def filter_data(df):
    # Filter for accidents with people killed
    df_filtered = df[df['UKATEGORIE'] == 1]

    return df_filtered

############################################

def cluster(df):
    # Remove rows with null values in 'LAT' or 'LNG' columns
    df = df.dropna(subset=['LAT', 'LNG'])

    # Convert latitude and longitude to radians for haversine distance calculation
    coords = df[['LAT', 'LNG']].to_numpy()
    kms_per_radian = 6371.0088

    ##############################
    # Only show if there are >5 points within 3km of each other
    epsilon = 3 / kms_per_radian
    ##############################

    # Check for NaN values in the coordinates
    if np.isnan(coords).any():
        raise ValueError("NaN values found in coordinates after dropping rows with NaNs")



    # Perform DBSCAN clustering
    db = DBSCAN(eps=epsilon, min_samples=5, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))

    # Add cluster labels to the dataframe
    df['cluster'] = db.labels_

    return df



# Function to convert UTM coordinates to latitude and longitude
def convert_utm_to_latlng(easting, northing, zone_number=32, zone_letter='N'):
    try:
        lat, lng = utm.to_latlon(easting, northing, zone_number, zone_letter)
    except:
        lat, lng = None, None
    return lat, lng

# Function to start a simple HTTP server and open the HTML file in the default web browser
def open_html_on_server(file_name, file_path='./', port=8000):
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = file_path
            return SimpleHTTPRequestHandler.do_GET(self)

    server_address = ('', port)
    httpd = HTTPServer(server_address, Handler)
    print(f"Serving {file_path} on http://localhost:{port}")
    webbrowser.open(f'http://localhost:{port}/{file_name}')
    httpd.serve_forever()

def main():
    # Get the file path from the command line arguments
    file_path = sys.argv[1]

    # Read the CSV file
    df = pd.read_csv(file_path)

    # Apply the conversion function to each row in the dataframe
    df[['LAT', 'LNG']] = df.apply(lambda row: convert_utm_to_latlng(row['LINREFX'], row['LINREFY']), axis=1, result_type='expand')

    df = filter_data(df)

    df = cluster(df)

    # Select the required columns
    df_selected = df[['LAT', 'LNG']]

    # Export the selected columns to a new CSV file
    df_selected.to_csv('exported_coordinates.csv', index=False)

    print("Converted UTM coordinates to lat/lng and exported to 'exported_coordinates.csv'")

    # Example usage
    html_file_name = 'show_on_map.html'
    open_html_on_server(file_name=html_file_name)

if __name__ == "__main__":
    main()