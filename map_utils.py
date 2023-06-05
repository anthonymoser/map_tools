import pandas as pd
import geopandas as gpd
from pydantic import BaseModel, validator
from typing import Optional
# import googlemaps 

class ChoroMap(BaseModel):
    title: str
    geo: dict
    gdf: gpd.GeoDataFrame
    metric_field: str
    location_field: str 
    polygon_label_field: str 
    color_scale: str 
    style: dict
    
    @validator('gdf')
    def is_gdf(cls, v):
        assert isinstance(v, gpd.GeoDataFrame)
        return v 
    
    class Config:
        arbitrary_types_allowed = True 

class MapLayer(BaseModel):
    name: Optional[str]
    outline: bool
    layer_style: dict 
    gdf: gpd.GeoDataFrame
    annotate: dict = {}
    @validator('gdf')
    def is_gdf(cls, v):
        assert isinstance(v, gpd.GeoDataFrame)
        return v 
    
    class Config:
        arbitrary_types_allowed = True


def google_maps_geocode(addr:dict):
    geocode_result = gmaps.geocode(f"{addr['address_line_1']}, {addr['city']}, {addr['state']}")
    try:
        return geocode_result[0]['geometry']['location']
    except Exception as e:
        return None
    
def get_points(df:pd.DataFrame, lat_field:str, lon_field:str, crs:str = None)->gpd.GeoDataFrame:
    points = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_field], df[lat_field]), crs=crs)
    return points 

def points_in_bounds(points:gpd.GeoDataFrame, bounds:gpd.GeoDataFrame, crs:str):
    if points.crs is not None:
        points = points.to_crs(crs)
    else:
        points = points.set_crs(crs)
        
    if bounds.crs:
        bounds = bounds.to_crs(crs)
    else:
        bounds = bounds.set_crs(crs)
        
    return gpd.sjoin(points, bounds, predicate='intersects')

def count_points(gdf:gpd.GeoDataFrame, group_field, value_field):
    return gdf.groupby(group_field).geometry.count().rename(value_field).reset_index()
    