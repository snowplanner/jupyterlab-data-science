'''Function that makes statistical analysis'''

import numpy as np

def stat_analysis_sd (input_gdf, ddof=1):
    """
    Makes a statistical analysis of the input snow_depth
      Parameters:
        input_gdf (GeoDataFrame)
        ddof (integer): degrees of liberty
      Returns:
        output_list (list): list containing the values studied for the list

    """
    points_list = input_gdf['snow_depth']
    output_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    #Basic measures:
    output_list[0] = np.min(points_list)
    output_list[1] = np.max(points_list)
    #Central tendency measures:
    mean_sd = np.mean(points_list)
    output_list[2] = mean_sd
    weighted_mean_sd = np.average(points_list)
    output_list[3] = weighted_mean_sd
    median_sd = np.median(points_list)
    output_list[4] = median_sd

    #Measures of variability:
    variance_sd = np.var(points_list, ddof=ddof)
    output_list[5] = variance_sd
    stand_dev_sd = np.std(points_list, ddof=ddof)
    output_list[6] = stand_dev_sd
    skewness_sd = points_list.skew()
    output_list[7] = skewness_sd
    ranges_sd = np.ptp(points_list)
    output_list[8] = ranges_sd

    #print('Basic measures:', '\n', 'Minimmum value: ', np.min(points_list), '\n', 'Maximmum value: ', np.max(points_list))
    #print('Central Tendency measures:', '\n', 'Mean: ', mean_sd,'\n' ,'Weighted mean: ', weighted_mean_sd, '\n', 'Median: ', median_sd)
    #print('Variability measures:', '\n', 'Variance: ', variance_sd,'\n' ,'Standard Deviation: ', stand_dev_sd, '\n', 'Skewness: ', skewness_sd, '\n', 'Ranges: ', ranges_sd)

    return output_list
