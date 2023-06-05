from map_utils import ChoroMap
import matplotlib as mpl
import matplotlib.pyplot as plt
import contextily as ctx 
from pathlib import Path

fpath = Path(mpl.get_data_path(), "/Users/AnthonyMoser/Dev/public_data_tools/map_tools/fonts/BigShouldersText-Thin.ttf")

def get_mpl_choropleth(map: ChoroMap):
    
    fig, ax = plt.subplots(1, figsize=(20, 20))
    ax.set_title(map.title, fontdict={'fontsize': '24', 'font':fpath, 'fontweight' : 3})
    ax.annotate('A PublicDataTools Map', xy=(1.06,-.02), xycoords='axes fraction', font=fpath, fontsize=13, color='black')
    
    sm = plt.cm.ScalarMappable(cmap=map.color_scale, norm=plt.Normalize(vmin=map.gdf[map.metric_field].min(), vmax = map.gdf[map.metric_field].max()))
    fig.colorbar(sm, ax=plt.gca())
    
    for s in ax.spines:
        ax.spines[s].set_color('lightgrey')
    ax.tick_params(colors='lightgrey', which='both')  # 'both' refers to minor and major axes
    
    map.gdf['coords'] = map.gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
    map.gdf['coords'] = [coords[0] for coords in map.gdf['coords']]

    for idx, row in map.gdf.iterrows():
        plt.annotate(text=row[map.polygon_label_field], xy=row['coords'],horizontalalignment='center', size=7)
    choro = map.gdf.plot(figsize=(20,20), column=map.metric_field, cmap=map.color_scale, ax=ax)
    fig.savefig(f'exports/{map.title}.png',bbox_inches='tight', dpi=300)         
    return fig, choro


def layer_map(map_layers:list, show_base_map:bool, filename:str, title:str, fig = None, ax = None):
    crs = map_layers[0].gdf.crs
    
    # Prep the plot
    if fig is None and ax is None:
        fig, ax = plt.subplots(1, figsize=(20, 20), facecolor="white")
    
    ax.set_aspect('equal')
    ax.autoscale(enable=True)
    
    plt.title(title, fontdict={'fontsize': '24', 'font':fpath, 'fontweight' : 3})
    
    for z, m in enumerate(map_layers):
        if m.gdf.crs is None:
            m.gdf = m.gdf.set_crs(crs)
        elif m.gdf.crs != crs:
            m.gdf = m.gdf.to_crs(crs)
        
        if m.outline:
            m.gdf.boundary.plot(ax = ax, zorder = z, **m.layer_style)
        else:
            m.gdf.plot(ax=ax, zorder = z, **m.layer_style)
        if len(m.annotate) > 0:
            m.gdf['coords'] = m.gdf['geometry'].apply(lambda x: x.representative_point().coords[:])
            m.gdf['coords'] = [coords[0] for coords in m.gdf['coords']]
            for idx, row in m.gdf.iterrows():
                plt.annotate(text=row[m.annotate['label_field']], xy=row[m.annotate['coords']],horizontalalignment='center', color= "lightgrey", size=7)
                    
    if show_base_map:
        ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
        ax.axis('off')
        
    layered_map = plt.show()
    fig.savefig(f'exports/{title}.png',bbox_inches='tight', dpi=300)
    return