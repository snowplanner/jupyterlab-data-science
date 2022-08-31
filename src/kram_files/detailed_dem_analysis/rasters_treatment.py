#pylint: disable=no-name-in-module
'''
  Module containing functions to:
    - Create multiple classified rasters of a same zone
    - Polygonize the classified rasters and extract the main statistics
    - Extract the main statistics
'''

from osgeo import gdal
import numpy as np
import pandas as pd
from fundamental_functions_import import classify_rasters, points_into_polygons, statistics_kram


def create_all_classified_rasters (input_path_dem, input_slope_path, input_aspect_path,
  conditions, output_paths):
    """
    Creates a series of classified rasters, depending on the input conditions given
    Parameters:
      input_path_dem (string): dem saetde path, it is the raster base layer
      input_slope_path (string): dem saetde slope path
      input_aspect_path (string): dem saetde aspect path
      conditions (numpy matrix): matrix containing lists, each one defining the conditions
        for 1 raster
      output_paths (numpy_matrix): matrix containing lists, each one defining the output path
        where will be stored the raster
      len (integer): number of the total rasters (== len(conditions) or len(output_paths))
    """

    for rast_cond in enumerate(conditions):
        classify_rasters.classify_raster(input_path_dem, input_slope_path, input_aspect_path,
          conditions[rast_cond[0]], output_paths[rast_cond[0]])


def polygonize_and_stats (input_rasters_path, input_points_path):
    """
    For each raster path, the function polygonizes the raster, it checks which points are
      inside the polygons and finally calculates basic statistics
    Parameters:
      input_rasters_path (list): list containing the path for each raster
      input_points_path (path): input path of the points that we want to classify into polygons
    Returns:
      stats_list (list): list containing the results as GeoDataFrames
    """

    stats_list = []
    empty_list = []

    for raster_path in enumerate(input_rasters_path):
        raster = gdal.Open(input_rasters_path[raster_path[0]])

        if raster is not None:
            rast_array = raster.GetRasterBand(1).ReadAsArray()
            if rast_array is not None:
                polygonized_rast = points_into_polygons.polygonize_raster(input_rasters_path[raster_path[0]])
                classified_points = points_into_polygons.points_into_polys(polygonized_rast, input_points_path)
                classified_points = points_into_polygons.pretty_gdf(classified_points)

                if classified_points.empty:
                    stats_list.append(empty_list)
                else:
                    statistics = statistics_kram.stat_analysis_sd(classified_points)
                    stats_list.append(statistics) # I did not do it firstly
            else:
                stats_list.append(empty_list)

        else:
            stats_list.append(empty_list)

    return stats_list


def get_statistics (gdf_list_path):
    """
    Despite the polygonize_and_stats function, this one, only gives the statistics when all the
      gdf associated to the rasters are already created
    Parameters:
      gdf_list_path (list): list containing empty lists or gdf with the data of the
        points_into_polygons
    Returns:
      statistics_list (list): list containing several lists, empty ones or those having the main
        statistical characteristics of each raster
    """

    gdf_list = np.load(gdf_list_path, allow_pickle=True)
    statistics_list = []

    for element in enumerate(gdf_list):
        empty_list = []
        list_element = gdf_list[element[0]]

        if any(list_element):
            stats = statistics_kram.stat_analysis_sd(list_element)
            statistics_list.append(stats)
        else:
            statistics_list.append(empty_list)

    return statistics_list


def create_gdf_stats (statistics_path, cr_path_list):
    """
    Takes the statistical characteristics being in a list, and creates a dataframe with it
    Parameters:
      statistics_path (string): path were the statistics extracted are stored
      cr_path_list (string): path were the classified rasters paths are stored
    Returns:
      stats_df (pandas DataFrame): dataframe containing the information extracted
    """

    stats_list = np.load(statistics_path, allow_pickle=True)
    cr_paths = np.load(cr_path_list, allow_pickle=True)

    aspect = ""; height= ""; slope= ""
    aspect_str_list = ['north', 'south', 'west', 'east']
    height_str_list = ['1900_2000', '2000_2100', '2100_2200', '2200_2300', '2300_2400', 
      '2400_2500', '2500_2700']
    slope_str_list = ['0_5', '5_10', '10_15', '15_20', '20_25', '25_30', '30_40', '40_90']

    stats_df = pd.DataFrame(stats_list)
    stats_df = pd.DataFrame(stats_df[0].to_list(), columns=['Min', 'Max', 'Mean', 'Weighted_Mean',
      'Median', 'Variance', 'Standard_Dev', 'Skeweness', 'Ranges'])
    stats_df.reset_index()
    stats_df['index'] = cr_paths
    stats_df= stats_df.assign(Aspect=aspect, Height=height, Slope=slope)

    for aspect in enumerate(aspect_str_list):
        stats_df['Aspect'].loc[stats_df['index'].str.contains(aspect_str_list[aspect[0]])] = aspect_str_list[aspect[0]]

    for height in enumerate(height_str_list): 
        stats_df['Height'].loc[stats_df['index'].str.contains(height_str_list[height[0]])] = height_str_list[height[0]]

    for slope in enumerate(slope_str_list): 
        stats_df['Slope'].loc[stats_df['index'].str.contains(slope_str_list[slope[0]])] = slope_str_list[slope[0]]
    
    return stats_df
