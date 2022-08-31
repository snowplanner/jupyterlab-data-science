This repository is dedicated to the study and manipulation of rasters and geometries of a terrain. 
The ultimate goal is to classify a terrain, study it, and extract its basic properties.
Nevertheless, a lot of intermediate steps and multiple functions are created in order to be able to be adaptative to other projects having its own goals. 

The main structure of the repository consists in different folders grouped by functionalities and degree of nested functions employed.
Also, some notebooks are included in the folders, in order to have some examples on how to employ the functions described.

Detailed structure:
  1. 'dem_utils' folder: implements the most basic functions to work with rasters and geojson functionalities

  2. 'fundamental_functions' folder: implements more complex functions to perform calculations and operations into rasters and geojson files, and extracts interesting statistics of the terrain

  3. 'detailed_dem_analysis' folder: devoted to make an extensive analysis of a general terrain, that will be divided in multiple rasters, each one having very particular conditions

  4. 'specific_dem_analysis' folder: devoted to make an extensive analysis of a very particular portion of a terrain

  5. 'examples_gdal' folder: devoted to give an insight on how to make the most basic manipulations on a raster and shapefiles 

  5. 'inputs' folder: contains the files being previous to the projects

  6. 'outputs' folder: contains the files created during the project

  7. 'saetde_Sw_prod.ipynb' notebook: extraction of snow depth data in the SnowPlanner project
