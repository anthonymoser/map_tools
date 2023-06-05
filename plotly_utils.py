from map_utils import ChoroMap
import plotly.graph_objects as go
import plotly 
import json 
import os 

zoom_styles = {
    "il": {
        "mapbox_zoom": 6.2,
        "mapbox_center":  {"lat":39.892142, "lon": -88.988653}
    },
    "chicago": {
        "mapbox_zoom": 10.6,
        "mapbox_center": {"lat":41.8823348, "lon": -87.6282938}   
    }
}

def get_geojson(boundary_file):
    if boundary_file[-7:] != "geojson":
        gdf = gpd.read_file(boundary_file)
        boundary_file = f"{boundary_file.split('.')[0]}.geojson"
        gdf.to_file(boundary_file)
        
    with open (boundary_file) as data:
        bounds = json.load(data)
    return bounds 

def save_map(fig, filename):
    plotly.offline.plot(fig, filename)
    os.rename('temp-plot.html', filename)
    # temp-plot.html

def get_plotly_choropleth(map:ChoroMap):
# geo:str, df:pd.DataFrame, metric_field:str, location_field:str, style:dict, title:str, color_scale:str = 'Reds'
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=map.geo,
            locations=map.gdf[map.location_field],
            featureidkey=f"properties.{map.location_field}",
            z=map.gdf[map.metric_field],
            colorscale=map.color_scale,
            marker_opacity=0.7,
            marker_line_width=0,
            hovertemplate= '<b>%{z}</b><br><extra>%{location}</extra>'
        )
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        width=800,
        height=1000,
        title=map.title,
        hoverlabel = {"font": {"size": 14}},
        **map.style
    )
    
    return fig 