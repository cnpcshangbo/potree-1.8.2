import pyproj

utm_zone_18 = pyproj.Proj(init='epsg:32618') # Define the UTM Zone 18 projection
wgs84 = pyproj.Proj(init='epsg:4326')   # Define the WGS84 projection (used by GPS)

easting = 572272.30
northing = 4498557.23

longitude, latitude = pyproj.transform(utm_zone_18, wgs84, easting, northing)

print("Longitude:", longitude)
print("Latitude:", latitude)
