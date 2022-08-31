The module 'dem_utils' contains the basic functionalities to work and manipulate rasters and shapefiles. It also includes some functions to make calculations into a raster.

In this folders, you will encounter the following modules:
  1. 'import_export_rasters_module': load and write rasters
    - 'open_raster_array'
    - 'write_raster_array'
    - 'write_raster_rasterio'

  2. 'load_write_geojson_module': load and write shapefiles and geojson files
    - 'load_json_file'
    - 'load_geom_json'
    - 'load_shapefile_geometries'
    - 'write_geojson'
    - 'write_shp'

  3. 'manipulate_threshold_vals_module': change threshold values in a raster
    - 'raster_threshold_to_0 '
    - 'raster_threshold_to_nan'
  
  4. 'flat_coords_module': remove third dimension for a set of coordinates
    - 'flat_point'
    - 'flat_linestring'
    - 'flat_polygon'
    - 'flat_multipolygon'
    - 'delete_z_coordinate'
  
  5. 'gdal_processing_module': different processings for rasters
    - 'calculate_slope_dem'
    - 'calculate_aspect_dem'
    - 'calculate_hillshade_dem'
  
  6. 'visualize_rasters_module': raster and shapefiles plotting
    - 'quick_show_rasterio'
    - 'plot_raster'
    - 'plot_base_layer_slopes'
