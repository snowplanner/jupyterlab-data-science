'''
Module containing functions to:
  - Hillshade calculation of a raster
  - Slope calciulation of a raster
  - Aspect calculation of a raster
'''

from osgeo import gdal
import rasterio


def calculate_slope_dem (in_file):
    """
      Calculates the slope of an input tiff file
      Parameters:
        in_file (string): path where it is stored the GeoTiff file
      Returns:
        slope (numpy array): raster array associated to the slope
    """
    gdal.DEMProcessing('slope.tif', in_file, 'slope')
    with rasterio.open('slope.tif') as dataset:
        slope = dataset.read(1)
    return slope


def calculate_aspect_dem (in_file):
    """
      Calculates the aspect of an input tiff file
      Parameters:
        in_file (string): path where it is stored the GeoTiff file
      Returns:
        aspect (numpy array): raster array associated to the aspect
    """
    gdal.DEMProcessing('./outputs/rasters/aspect_raster.tif', in_file, 'aspect')
    with rasterio.open('./outputs/rasters/aspect_raster.tif') as dataset:
        aspect = dataset.read(1)
    return aspect


def calculate_hillshade_dem (in_file):
    """
      Calculates the hillshade of an input tiff file
      Parameters:
        in_file (string): path where it is stored the GeoTiff file
      Returns:
        hillshade (numpy array): raster array associated to the hillshade
    """
    gdal.DEMProcessing('./outputs/rasters/hillshade_raster.tif', in_file, 'hillshade')
    with rasterio.open('./outputs/rasters/hillshade_raster.tif') as dataset:
        hillshade = dataset.read(1)
    return hillshade
