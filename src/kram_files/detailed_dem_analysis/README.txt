The module 'detailed_dem_analysis' contains several functions to perform an extensive analysis of a terrain subdivided in rasters with very specific conditions and also an illustrative notebook on how to employ those functions

In this folder, you will encounter the following modules/notebooks:
  1. 'dem_utils_import.py': 
    - import functions from module 'dem_utils'
  
  2. 'fundamental_functions_import.py':
    - import functions from module 'fundamental_functions'
  
  3. 'list_creator.py': creates different lists, to define the inputs for each raster and teh output paths
    - 'height_list'
    - 'slope_list'
    - 'cond_matrix'
    - 'output_path_list'
    - 'collect_paths'
  
  4. 'rasters_treatment.py': automatization of the 'fundamental_functions' module to create automatically several rasters
    - 'create_all_classified_rasters'
    - 'polygonize_and_stats'
    - 'get_statistics'
    - 'create_gdf_stats'
  
  5. 'test_functions.ipynb': tests the previous functions
