''''''

import rasterio
import numpy as np
import imageio
from dem_utils_import import load_rast, gdal_process


def check_processus (features, dem_path, out_tif_path, out_tif_path_imageio, out_slope_path, out_aspect_path, datatype='float32', ndv=None):
    """Check if the geoclassifying functions work well"""
    raster = rasterio.open(dem_path)

    out_image, out_transform = rasterio.mask.mask(raster,
    features, crop=True, filled=True, invert=False)
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

    #Resave it:
    out_tif = load_rast.open_raster_array(out_tif_path)
    load_rast.write_raster_array(out_tif, dem_path, out_tif_path)

    #Calculate Slope and Aspect
    slope_trail = gdal_process.calculate_slope_dem(out_tif_path_imageio, out_slope_path)
    slope_trail_nodata = np.where(slope_trail==-9999., np.nan, slope_trail)
    load_rast.write_raster_array(slope_trail_nodata, out_tif_path, out_slope_path)

    aspect_trail = gdal_process.calculate_aspect_dem(out_tif_path, out_aspect_path)
    aspect_trail_nodata = np.where(aspect_trail==-9999., np.nan, aspect_trail)
    load_rast.write_raster_array(aspect_trail_nodata, out_tif_path, out_aspect_path)


def get_properties (input_raster_path, input_slope_path, input_aspect_path):
    """Extracts the general porperties of a desired terrain"""

    #Height Data
    height_raster_arr = load_rast.open_raster_array(input_raster_path)
    height_raster_arr = np.where(height_raster_arr >= 3.3999e38, np.nan, height_raster_arr)
    height_raster_arr = np.nan_to_num(height_raster_arr)
    height = height_raster_arr[np.where(height_raster_arr != 0.)]
    avg_height = np.mean(height); max_height = np.max(height); min_height = np.min(height)

    #Slope Data
    slope_raster_arr = load_rast.open_raster_array(input_slope_path)
    slope_raster_arr = np.nan_to_num(slope_raster_arr)
    slope = slope_raster_arr[np.where(slope_raster_arr != 0.)]
    avg_slope = np.mean(slope); max_slope = np.max(slope); min_slope = np.min(slope)

    #Aspect Data
    aspect_raster_arr = load_rast.open_raster_array(input_aspect_path)
    aspect_raster_arr = np.nan_to_num(aspect_raster_arr)
    aspect = aspect_raster_arr[np.where(aspect_raster_arr != 0.)]
    avg_aspect = np.mean(aspect); max_aspect = np.max(aspect); min_aspect = np.min(aspect)

    return [avg_height, min_height, max_height, avg_slope, min_slope, max_slope, avg_aspect, min_aspect, max_aspect]
