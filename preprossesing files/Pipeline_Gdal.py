from osgeo import gdal, ogr
import os
import time

input_polygon_layer = r'C:/Users/paco_/OneDrive/Escritorio/SIG 2023/Reconquista/Lago San Francisco/Reconquista_completo.geojson'
params = ["pH", "OD", "EC", "TDS", "T"]

for p in params:

    clipped_raster = f"C:/Users/paco_/OneDrive/Escritorio/SIG 2023/Pythonproject/outputs/Final{p}.tif"
    # clipped_raster = f"C:/Users/paco_/OneDrive/Escritorio/Final{p}.tif"

    # inverse distance to a power
    idw = gdal.Grid("", r"C:\Users\paco_\OneDrive\Escritorio\SIG 2023\Reconquista\Puntos\sitios.shp", zfield=p,
                    algorithm="invdist:nodata=-9999",
                    format='MEM',
                    outputBounds=[-58.899568231, -34.389464318, -58.578032082, -34.707894107],
                    width=16078, height=15922,
                    )

    # Clip the raster with the polygon using gdal.Warp
    clip = gdal.Warp(clipped_raster, idw, cutlineDSName=input_polygon_layer, cropToCutline=True)