# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import geopandas as gpd
import folium
import matplotlib.pyplot as plt

gdf = gpd.read_file(r"C:\Users\ALFAFA\Desktop\Final\mygeodata\database.gpkg")

m = folium.Map(location=[19.124589, 74.724012], zoom_start=13)

#Get unique list of SWM types
unique_swm_types = list(set(gdf.Type))
icon_colors=['darkgreen', 'purple', 'black', 'lightblue', 'beige', 'cadetblue', 'green', 'blue', 'lightred', 'red', 'lightgreen', 'lightgray', 'orange', 'darkpurple', 'darkblue', 'pink', 'white', 'gray', 'darkred']



for index, row in gdf.iterrows():
    for ind, ind_color in enumerate(unique_swm_types): 
        if row.Type == ind_color:
            
            marker_color = icon_colors[ind]
            
            folium.Marker(
                location=[row.latitude, row.longintude],
                popup=row['Type'],
                icon=folium.Icon(color=marker_color)    
            ).add_to(m)
            
           
    

m.save("file.html")