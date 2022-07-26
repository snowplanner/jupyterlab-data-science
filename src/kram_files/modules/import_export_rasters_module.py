'''
Module containing functions to:
  - Open the array associated to a raster.
  - Write an array into a tiff file.
'''

import sys
from osgeo import gdal
import rasterio
import numpy as np
import affine


def open_raster_array(input_tiff, nb_raster_band=1):
    """
      Opens the array asssociated to the raster.
      Parameters:
        input_tiff (string): path of the tiff image
        nb_raster_band (integer): number of the raster band
      Returns:
        dem_array (numpy array): the associated array of the tiff image
    """
    dem_file = gdal.Open(input_tiff)
    dem_array = dem_file.GetRasterBand(nb_raster_band).ReadAsArray()
    return dem_array


def write_raster_array (raster_array, original_tif_path, output_path, nb_raster_band=1):
    """
      Saves the numpy array into a GeoTiff file and keeps the metadata from the original Tiff
      Parameters:
        raster_array (numpy array): array to be saved
        original_tiff_path (string): original tiff to copy the metadata
        output_path (string): path where the saving is made
        nb_raster_band (integer): raster band
    """
    original_tif = gdal.Open(original_tif_path)
    if original_tif is None:
        print('Could not open the image file')
        sys.exit(1)
    rows = original_tif.RasterYSize
    cols = original_tif.RasterXSize
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
    geotrans = original_tif.GetGeoTransform()
    projection = original_tif.GetProjection()
    out_dataset.SetGeoTransform(geotrans)
    out_dataset.SetProjection(projection)
    out_dataset.GetRasterBand(nb_raster_band). WriteArray(raster_array)

    out_dataset.FlushCache()
    out_dataset = None


def write_raster_rasterio (array, input_tif_path, output_path, crs='EPSG:4326'):
    """
      Saves the numpy array into a GeoTiff file, done with rasterio
      Parameters:
        array (numpy array): areray to be saved
        input_tif_path (string): original tiff to copy the metadata
        output_path (string): path where the savig is done
        crs (string): CRS code of the system
    """
    dem_tif = gdal.Open(input_tif_path)
    raster_crs = crs
    output_array = np.float32(array)
    geo_transform_input = dem_tif.GetGeoTransform()
    afn = affine.Affine.from_gdal(*geo_transform_input)
    with rasterio.open(
      output_path,
      'w',
      driver='GTiff',
      height=np.shape(output_array)[0],
      width=np.shape(output_array)[1],
      count=1,
      dtype=np.float32,
      crs=raster_crs,
      transform=afn) as tif_file:
        tif_file.write(output_array,1)
    tif_file.close()
