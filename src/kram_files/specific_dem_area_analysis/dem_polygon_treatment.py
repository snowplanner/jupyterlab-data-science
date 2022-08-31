'''
  Module containing functions to:
    - Select a polygon
    - Make the proper analysis to such polygon
    - Polygonize a raster, check which points are inside the polygon and calculate its statistics
'''

import numpy as np
import imageio
import rasterio
from fundamental_functions_import import points_into_polygons, statistics_kram 
from dem_utils_import import load_json, gdal_process, load_rast, flat


def select_slope (input_trails_path, input_slope_name):
    """
    Selects and loads the geometry of the desired slope in the ski resort
    Parameters:
      input_trails_path (string): path where it is stored the shapefile containing the polygons
      input_slope_name (string): name associated to the desired polygon
    Returns:
      trails_slope (geojson): shapefile defining the polygon
    """

    trails_3d = load_json.load_json_file(input_trails_path)
    trails_slope = []

    for slope in range(len(trails_3d['features'])):
        if trails_3d['features'][slope]['properties']['trail_code'] == input_slope_name:
            trails_slope = trails_3d['features'][slope]

    return trails_slope


def prepare_slope (input_trail, input_dem_path, out_tif_path, out_tif_path_imageio, out_slope_path, out_aspect_path, ndv=None, datatype='float32'):
    """
    From an input polygon, it will give a raster sense to it and do the pertinent analysis
    Parameters:
      input_trail (geojson): shapefile defining the input polygon
      input_dem_path (string): path where it is stored the dem of the area
      out_tif_path (string): path where will be stored the cropped dem
      out_tif_path_imageio (string): path where will be stored the cropped dem (w/ imageio library)
      out_slope_path (string): path where will be stored the slope dem
      out_aspect_path (string): path where will be stored the aspect path
    """

    #Delete Z coordinate
    out_trail = input_trail.copy()
    geometry_coords = out_trail['geometry']['coordinates']
    coords_2d = flat.flat_multipolygon(geometry_coords)
    out_trail['geometry']['coordinates'] = coords_2d

    #Crop Raster
    geometry_trail = [out_trail['geometry']]
    raster = rasterio.open(input_dem_path)

    out_image, out_transform = rasterio.mask.mask(raster,
        geometry_trail, crop=True, filled=True, invert=False)
    out_meta = raster.meta.copy()
    out_image = np.ma.masked_where(out_image == ndv, out_image)
    out_meta.update({'driver': 'GTiff', 'height': out_image.shape[1],
                  'width': out_image.shape[2], 'transform': out_transform,
                  'nodata': ndv, 'dtype': datatype, 'tiled': True,
                  'blockxsize': 128, 'blockysize': 128})
    with rasterio.open(out_tif_path, 'w', **out_meta) as dest:
        dest.write(out_image)

    #Save it with imageio
    trail_rast = load_rast.open_raster_array(out_tif_path)
    imageio.imwrite(out_tif_path_imageio, trail_rast)

    #Calculate Slope and Aspect
    slope_trail = gdal_process.calculate_slope_dem(out_tif_path_imageio, out_slope_path)
    slope_trail_nodata = np.where(slope_trail==-9999., np.nan, slope_trail)
    load_rast.write_raster_array(slope_trail_nodata, out_tif_path, out_slope_path)

    aspect_trail = gdal_process.calculate_aspect_dem(out_tif_path, out_aspect_path)
    aspect_trail_nodata = np.where(aspect_trail==-9999., np.nan, aspect_trail)
    load_rast.write_raster_array(aspect_trail_nodata, out_tif_path, out_aspect_path)


def poly_and_statistics (input_tif_path, points_to_filter_path, input_slope_name):
    """
    Polygonizes a raster, check which points are inside the polygon and calculate its
     intrinsic statistics
    Parameters:
      input_tif_path (string): path where it is stored the tif file to polygonize
      points_to_filter_path (string): path where it is stored the dataframe containing the points
      input_slope_name (string): name associated to the desired polygon
    Returns:
      stats_trail (list): contains the statistics associated to the points inside the polygon
    """
    trail_polygons = points_into_polygons.polygonize_raster(input_tif_path)
    trail_points = points_into_polygons.points_into_polys(trail_polygons, points_to_filter_path)
    trail_points = points_into_polygons.pretty_gdf(trail_points)
    trail_points = trail_points[trail_points.trail_code == input_slope_name].reset_index(drop=True)
    stats_trail = statistics_kram.stat_analysis_sd(trail_points)

    return stats_trail
