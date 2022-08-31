'''
Module containing functions to:
  - Plot a raster with matplotlib and rasterio.
  - Save the obtained images.
'''

import rasterio
import rasterio.plot as rp
import matplotlib.pyplot as plt
import geopandas as gpd
import import_export_rasters_module as fm1


def quick_show_rasterio (tiff_path, nb_raster_band=1):
    """
      Array visualization with the package module rasterio
      Parameters:
        tiff_path (string): path where it is stored the tiff file
        nb_raster_band (integer): number of the raster band we want to work with
    """
    tiff_file = rasterio.open(tiff_path)
    rp.show((tiff_file, nb_raster_band), cmap='terrain')


def plot_raster(input_file_path, image_path, title, cmap, nb_raster_band=1):
    """
      Array visualization with the package module matplotlib
      Parameters:
        input_file_path (string): path where it is stored the tiff file
        image_path (string): path where the image will be saved
        title (string): title of the plot
        cmap (string): color palette that we want to employ to represent the data
        nb_raster_band (integer): number of the raster band we want to work with
    """
    array = fm1.open_raster_array(input_file_path, nb_raster_band)
    plt.figure(figsize=(15,7))
    plt.imshow(array)
    plt.colorbar()
    plt.set_cmap(cmap)
    plt.title(title)
    plt.savefig(image_path, dpi= 1000)
    plt.show()


def plot_base_layer_slopes (base_layer_path, input_shp_file):
    """
      Trails visualizatipon with the dem file background
      Parameters:
        base_layer_path (string): path where it is stored the tiff file
        input_shp_file (string): path where it is stored the shapefile
    """
    base_map = rasterio.open(base_layer_path)
    shape_gdf = gpd.read_file(input_shp_file)
    ax = plt.subplots(figsize=(15,15))
    ax = rasterio.plot.show(base_map, with_bounds = True, ax=ax, cmap='magma')
    shape_gdf.plot(ax=ax, cmap = 'Greys_r')
    plt.title('Saetde slope trails w/ the base layer')
