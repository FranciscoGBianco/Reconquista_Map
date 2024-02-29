import rioxarray as rxr
import datashader as ds
import datashader.transfer_functions as tf
from colorcet import rainbow4
from pyproj import Transformer

def process_raster(raster_file, name=""):
    dtm_pre_arr = rxr.open_rasterio(raster_file, masked=True).squeeze().rio.reproject('EPSG:3857')

    converted_df = dtm_pre_arr.to_dataframe(name=name).reset_index()

    return converted_df.dropna().reset_index(drop=True)


def get_mapbox_layer(df_in, cmap_col=rainbow4, name='', span_range=None, save=False):
    if span_range is None:
        span_range = [0, 10]

    meshgrid_cols = [int(df_in['x'].nunique() * 0.8), int(df_in['y'].nunique() * 0.8)]
    # code to ensure that the canvas is not larger than the data available
    cvs = ds.Canvas(plot_width=min(meshgrid_cols[0], 3200), plot_height=min(meshgrid_cols[1], 2000))

    agg = cvs.points(df_in, agg=ds.mean(name), x='x', y='y')
    # We set the aggregation method to take the mean value
    agg = cvs.raster(agg, interpolate='linear')

    coords_lat, coords_lon = agg.coords['y'].values, agg.coords['x'].values
    # print(coords_lon)
    # print(coords_lat)

    gcs_to_4326 = Transformer.from_crs(3857, 4326, always_xy=True)
    # We use pyproj to create a transformer to covert the corner coordinates
    # This ensures that the output image object can be displayed on the map
    lon_min, lat_min = gcs_to_4326.transform(coords_lon[0], coords_lat[-1])
    lon_max, lat_max = gcs_to_4326.transform(coords_lon[-1], coords_lat[0])

    coordinates = [[lon_min, lat_min],
                   [lon_max, lat_min],
                   [lon_max, lat_max],
                   [lon_min, lat_max]]

    img_out = tf.shade(agg, cmap=cmap_col, how="linear", span=span_range).to_pil()

    if save:
        img_out.save(f"{name[0:2]}.tif")

    return [{"below": 'traces', "sourcetype": "image", "source": img_out, "coordinates": coordinates,
            "opacity": 0.85}]
