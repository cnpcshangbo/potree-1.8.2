import pyproj
from PIL import Image
from PIL.ExifTags import TAGS

utm_zone_18 = pyproj.Proj(init='epsg:32618') 
wgs84 = pyproj.Proj(init='epsg:4326')   

def get_exif_data(image_path):
    """Extracts GPS information from the EXIF data of an image."""
    image = Image.open(image_path)
    exif_data = image._getexif()

    if exif_data:  
        gps_info = exif_data.get(34853)  # Get the GPSInfo tag

        # Extract latitude and longitude with rational degree conversion
        lat_data = gps_info[2] 
        lon_data = gps_info[4] 

        # Convert IFDRational to decimal degrees
        lat_degrees = lat_data[0].numerator / lat_data[0].denominator
        lat_minutes = lat_data[1].numerator / lat_data[1].denominator
        lat_seconds = lat_data[2].numerator / lat_data[2].denominator 

        lon_degrees = lon_data[0].numerator / lon_data[0].denominator 
        lon_minutes = lon_data[1].numerator / lon_data[1].denominator 
        lon_seconds = lon_data[2].numerator / lon_data[2].denominator 

        # Adjust latitude and longitude based on N/S and E/W indicators 
        latitude = (lat_degrees + lat_minutes/60 + lat_seconds/3600) * (1 if gps_info[1] == b'N' else -1)
        longitude = (lon_degrees + lon_minutes/60 + lon_seconds/3600) * (1 if gps_info[3] == b'E' else -1)

        return latitude, longitude
    else:
        return None

def convert_gps_to_utm(image_path):
    """Reads GPS from EXIF, converts to UTM Zone 18, and prints the results."""
    latitude, longitude = get_exif_data(image_path)

    if latitude and longitude:
        easting, northing = pyproj.transform(wgs84, utm_zone_18, longitude, latitude)
        print("Easting:", easting)
        print("Northing:", northing)
    else:
        print("No GPS data found in the image.")

# Example usage
image_path = "/home/roboticslab/Downloads/OneDrive_2024-02-03/NYCSpan8-9/raw/images/S1074589.JPG" 
convert_gps_to_utm(image_path) 
