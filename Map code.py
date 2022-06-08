# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 17:16:33 2022

@author: ALFAFA
"""

import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import tkinter
from tkinter import Frame

gdf = gpd.read_file(r"C:\Users\ALFAFA\Desktop\S4GE g6\MAP\database table.gpkg")
m = folium.Map(location=[19.124589, 74.724012], zoom_start=15.3, attr="<a href=https://endless-sky.github.io/>Endless Sky</a>")


#Get unique list of SWM types and make markers for the points

unique_swm_types = list(set(gdf.Type))

icon_colors=['darkgreen', 'purple', 'black', 'lightblue', 'beige', 'cadetblue', 'green', 'blue', 'lightred', 'red', 'lightgreen', 'lightgray', 'orange', 'darkpurple', 'darkblue', 'pink', 'white', 'gray', 'darkred']

for index, row in gdf.iterrows():
    for ind, ind_color in enumerate(unique_swm_types):
        if row.Type == ind_color:
            marker_color = icon_colors[ind]
            html=f"""
                    <body style="background-color:#e9f5f8;">
                        <h3><u> {row.Type} </u></h3>
                        <p>
                            <strong>
                                Location of Site: 
                            </strong>
                            
                            {row.latitude, row.longintude}
                        </p>
                        <p>
                            <strong>
                                Remarks:
                            </strong>
                            
                                {row.Remarks}
                        </p>
                    </body>
                  """
                  
#Create frame window when clicking on the point
            iframe = folium.IFrame(html=html, width=250, height=150)
            popup = folium.Popup(iframe)       
            folium.Marker(
                location=[row.latitude, row.longintude],
                popup=popup,
                icon=folium.Icon(color=marker_color)
            ).add_to(m)

 

m.save("file.html")
