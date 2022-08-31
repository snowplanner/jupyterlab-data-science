The module 'specidem_analysis' contains several functions to perform an specific analysis into a raster (in our case a ski slope) and also includes an illustrative notebook on hoy to employ such functions

In this folder, you will encounter the following modules/notebooks:
  1. 'dem_utils_import.py': 
    - import functions from module 'dem_utils'
  
  2. 'fundamental_functions_import.py':
    - import functions from module 'fundamental_functions'
  
  3. 'dem_polygon_treatment.py': selects a input geometry and makes all the process in order to extract useful statistics
    - 'select_slope'
    - 'prepare_slope'
    - 'poly_and_statistics'
  
  4. 'automatization': encompasses the previous functions into more automatizied functions, and extracts more statistics
    - 'get_stats_trail'
    - 'get_stats_pctg'
    - 'num_to_pctg'

  5. 'test_functions.ipynb': tests the previous functions and plots the results

  6. 'clssify_maps.ipynb': notebook in development to classify a terrain in smaller geometries
