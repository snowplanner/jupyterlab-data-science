'''
Module containing functions to:
  - Crop a tiff file employing a mask being a shp/geojson file
'''

import rasterio
import fiona
import numpy as np


def mask_by_shape(raster_file, shape_file, out_file_path, datatype='float32', ndv=None):
    """
      Crops an input tiff file using as a mask the input shapefile
      Parameters:
        raster_file (string): path where it is stored the raster file
        shape_file (string): path where it is stored the shapefile
        out_file_path (string): path where it will be saved the neww GeoTiff file
        datatype (string): specification of the type of data introduced in the metadata
        ndv (string)
    """
    raster = rasterio.open(raster_file)
    with fiona.open(shape_file, 'r') as shape:
        features = [feature['geometry'] for feature in shape if feature['geometry']]

    out_image, out_transform = rasterio.mask.mask(raster,
        features, crop=True, filled=True, invert=False)
    out_meta = raster.meta.copy()
    out_image = np.ma.masked_where(out_image == ndv, out_image)
    out_meta.update({'driver': 'GTiff', 'height': out_image.shape[1],
                  'width': out_image.shape[2], 'transform': out_transform,
                  'nodata': ndv, 'dtype': datatype, 'tiled': True,
                  'blockxsize': 128, 'blockysize': 128})
    with rasterio.open(out_file_path, 'w', **out_meta) as dest:
        dest.write(out_image)
