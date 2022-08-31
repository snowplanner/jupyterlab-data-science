'''
Module containing functions to:
  - Manipulate the threshold values of a raster
'''

from osgeo import gdal
import numpy as np

def raster_threshold_to_0 (input_tif, nb_raster_band=1):
    """
      Convert the threshold raster values into 0.
      Parameters:
        input_tif (string): path where it is stored the tiff file
        nb_raster_band (integer): number of the raster band we want to work with
      Returns:
        dem_array (numpy array): the new array without the threshold values reassigned
    """
    dem_file = gdal.Open(input_tif)
    dem_array = dem_file.GetRasterBand(nb_raster_band)
    no_data_val = dem_array.GetNoDataValue()
    dem_array = dem_array.ReadAsArray() 
    dem_array[dem_array==int(no_data_val)] = 0
    return dem_array

def raster_threshold_to_nan (input_tif_path, nb_raster_band=1):
    """
      Convert the threshold raster values into np.NaN.
      Parameters:
        input_tif_path (string): path where it is stored the tiff file
        nb_raster_band (integer): number of the raster band we want to work with
      Returns:
        dem_array (numpy array): the new array with the threshold values reassigned
    """
    dem_file = gdal.Open(input_tif_path)
    dem_array = dem_file.GetRasterBand(nb_raster_band)
    no_data_val = dem_array.GetNoDataValue()
    dem_array = dem_array.ReadAsArray()
    dem_array[dem_array==int(no_data_val)] = np.nan
    return dem_array
