'''
  Module containing functions to:
    - Automatize the processus that we can do with the other function module
'''

import numpy as np
from dem_polygon_treatment import select_slope, prepare_slope, poly_and_statistics
from dem_utils_import import load_rast


def get_stats_trail (input_trails_path, input_slope_name, input_dem_path, out_tif_path, out_tif_path_imageio, out_slope_path, out_aspect_path, points_to_filter_path, ndv=None, datatype='float32'):
    """
    Gives the statistics of a desired slope
      For more information consult the dem_polygon_treatment function module
    """

    #General Statistics
    trail = select_slope(input_trails_path, input_slope_name)
    prepare_slope(trail, input_dem_path, out_tif_path, out_tif_path_imageio, out_slope_path, out_aspect_path)
    stats = poly_and_statistics(out_tif_path, points_to_filter_path, input_slope_name)
    return stats


def get_stats_pctg (input_dem, input_slope, input_aspect, list_h, list_s, list_a):
    """
    Gives the statistics of a dem in percentatges
    Parameters:
      input_dem (tiff): dem that we want to get the statistics
      input_slope (tiff): slope dem that we want to get the statistics
      input_aspect (tiff): aspect dem that we want to get the statistics
      list_h/s/a (list): lists defining the ranges where we want to pack the data, respectively
    Returns:
      final_stats (list): list with the results
    """

    rasters = [load_rast.open_raster_array(input_dem), load_rast.open_raster_array(input_slope), load_rast.open_raster_array(input_aspect)]
    list_iter = [np.array(list_h), np.array(list_s), np.array(list_a)]
    final_stats = []

    for list_id in enumerate(list_iter):
        stats_pctg = []
        raster = rasters[list_id[0]]
        for i in range(len(list_iter[list_id[0]])-1):
            min = list_iter[list_id[0]][i]
            max = list_iter[list_id[0]][i+1]
            vals = np.where((raster >= min) & (raster < max))
            count = np.count_nonzero(vals)
            stats_pctg.append(count)
        final_stats.append(stats_pctg)

    return final_stats


def num_to_pctg (input_list):
    """
    Converts a list of floats into percentatges
    Parameters:
      input_list (list): list that has to be expressed in percentatges
    Returns:
      output_list (list): list with the statistics converted to percentatges
    """

    out_list = input_list.copy()
    for i in enumerate(input_list):
        list_selected = input_list[i[0]]
        summ = sum(list_selected)
        for j in enumerate(list_selected):
            list_selected[j[0]] = list_selected[j[0]] / summ

    return out_list
