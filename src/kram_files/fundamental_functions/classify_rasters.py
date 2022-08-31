'''
  Module containing functions to:
    - Create a classified raster
'''

import numpy as np
from dem_utils_import import load_rast, gdal_process


def gdal_processing(input_dem_path, input_dem_imageio_path, output_slope_path, output_aspect_path):
    """
    Creates and saves properly the aspect and slope rasters
    Parameters:
      input_dem_path (string): path of the cropped dem
      input_dem_imageio_path (string): path of the cropped dem, saved with imageio
      ouput_slope_path (string): output path where will be stored the slope raster
      output_aspect_path (string): ouput path where will be stored the aspect raster
    """

    #We create the slope file associated to the input dem
    slope = gdal_process.calculate_slope_dem(input_dem_imageio_path, output_slope_path)
    slope_nodata = np.where(slope==-9999., np.nan, slope)

    load_rast.write_raster_array(slope_nodata, input_dem_path, output_slope_path)

    #We create the aspect file associated to the input dem
    aspect = gdal_process.calculate_aspect_dem(input_dem_path, output_aspect_path)
    aspect_nodata = np.where(aspect==-9999., np.nan, aspect)

    load_rast.write_raster_array(aspect_nodata, input_dem_path, output_aspect_path)


def classify_raster(dem_path, slope_path, aspect_path, input_conditions, output_path):
    """
    Classifies a raster by the height, the slope and the aspect
    Parameters:
      dem_path (string): path of the cropped dem (height analysis)
      slope_path (string): path of the slope dem
      aspect_path (string): path of the aspect dem
      input_conditions (list): list where there are specified the input conditions
    """

    # Height Classification:
    height_array = load_rast.open_raster_array(dem_path)
    height_array = np.where(height_array >= 3,399e38, np.nan)

    height_class = np.copy(height_array)
    height_class[np.where((height_array > input_conditions[0]) & (height_array <=
      input_conditions[1]))] = 1.
    height_class[np.where(height_class != 1.)] = 0.

    #Slope Classification:
    slope_array = load_rast.open_raster_array(slope_path)
    slope_class = np.copy(slope_array)
    slope_class[np.where((slope_array > input_conditions[2]) & (slope_array <=
      input_conditions[3]))] = 1.
    slope_class[np.where(slope_class != 1.)] = 0.

    #Aspect Classification:
    aspect_array = load_rast.open_raster_array(aspect_path)
    aspect_class = np.copy(aspect_array)
    if input_conditions[6] == 0:
        aspect_class[np.where((aspect_array > input_conditions[4]) &
          (aspect_array <= input_conditions[5]))] = 1.
    elif input_conditions[6] == 1.:
        aspect_class[np.where((aspect_array > input_conditions[5]) |
          (aspect_array <= input_conditions[4]))] = 1.
    aspect_class[np.where(aspect_class != 1.)] = 0.

    #Classified_raster:
    classified_raster = height_class * slope_class * aspect_class
    load_rast.write_raster_array(classified_raster, dem_path, output_path)

#TODO: change list input cond for dict
