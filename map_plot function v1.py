
#Function takes an input of a place ()
#Gets coordinates of a place
#Adds it to a list
#Has corressponding data in another list
# Plots a choropleth map

# name of place might be different (UK for united kingdom/ bharat for india)
# account for it or flag it


def plot_choropleth (places, data): #input data[location], data[desired_data]
    import geopandas as gpd
    import matplotlib.pyplot as plt
    from geopy.geocoders import Nominatim
    import folium
    from folium.plugins import MarkerCluster

    coordinates = []
    geolocator = Nominatim(user_agent="MyApp")
    for place in places:
        location = geolocator.geocode(place)
        coordinate = [location.latitude, location.longitude]
        coordinates.append(coordinate)

    m = folium.Map(location=coordinates, zoom_start=12)
    
    folium.Choropleth(
        geo_data=None,  # Since we don't have a shapefile, we set this to None
        data=data,
        columns=['places', 'data'],
        key_on='feature.id',  # Set key_on to 'feature.id' since we don't have a shapefile
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Data'
    ).add_to(m)
    
    # Step 3: Add marker clusters for the coordinates (optional)
    marker_cluster = MarkerCluster().add_to(m)
    for coord in coordinates:
        folium.Marker(coord).add_to(marker_cluster)
    
    # Step 4: Display the map
    return m
