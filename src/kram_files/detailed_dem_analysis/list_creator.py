'''
  Module containing functions to:
    - Create an automatic list for the different studied heights
    - Create an automatic list for the different studied slopes
    - Create an automatic list for the different studied aspects
    - Creates a matrix containing lists of all the rasters conditions that we want to create
    - Creates an automatic list of each output path for the raster
'''

import os


def height_list (initial_value_height=1900, next2last_value_height=2500, last_value_height=2700):
    """
    Creates an automatic list, defining the study values of the height raster
    Parameters:
      initial_value_height (integer): initial value of the height list
      next2last_value_height (integer): penultimate value of the height list
      last_value_height (integer): last value of the height list
    Returns:
      height_list (numpy matrix / list): height list, containing the different ranges of study
    """

    list_height = []
    while initial_value_height <= last_value_height:
        list_height.append(initial_value_height)
        if initial_value_height != next2last_value_height:
            initial_value_height = initial_value_height + 100
        elif initial_value_height == next2last_value_height:
            initial_value_height = initial_value_height + 200
    return list_height


def slope_list (initial_value_slope=0, third2last_value_slope=30, second2last_value_slope=40, 
    last_value_slope=90):
    """
    Creates an automatic list, defining the study values of the slope raster
    Parameters:
      initial_value_slope (integer): initial value of the slope list
      third2last_value_slope (inetger): third to last value of the slope list
      next2last_value_slope (integer): next to last value of the slope list
      last_value_slope (integer): last value of the slope list
    Returns:
      slope_list (numpy matrix / list): slope list, containing the different ranges of study
    """

    list_slope = []
    while initial_value_slope <= last_value_slope:
        list_slope.append(initial_value_slope)
        if initial_value_slope == third2last_value_slope:
            initial_value_slope = initial_value_slope + 10
        elif initial_value_slope == second2last_value_slope:
            initial_value_slope = initial_value_slope + 50
        else:
            initial_value_slope = initial_value_slope + 5

    return list_slope


def cond_matrix (h_list, s_list, a_list):
    """
    Creates an automatic matrix containing a list of conditions, each one defining the parameters
      for a raster
    Parameters:
      height_list (list): list containing the height ranges of study
      slope_list (list): list containing the slope ranges of study
      list_condition (list): initial values of the list that will have the raster limit values
      aspect_list (list): list containing the aspect ranges of study
    Returns:
      conditions_matrix (numpy matrix): matrix containing several list, each one containing the 
        parameters to create a specific raster
    """
    conditions_matrix = []
    list_condition = [0, 0, 0, 0, 0, 0, 1]

    for asp_deg in (range(len(a_list)-1)):
        list_condition=[0, 0, 0, 0, 0, 0, 1]
        list_condition[4] = a_list[asp_deg]
        list_condition[5] = a_list[asp_deg + 1]

        for slope_deg in (range(len(s_list)-1)):
            list_condition = [0, 0, 0, 0, a_list[asp_deg], a_list[asp_deg + 1], 1]
            list_condition[2] = s_list[slope_deg]
            list_condition[3] = s_list[slope_deg + 1]

            for height in (range(len(h_list)-1)):
                list_condition = [0, 0, s_list[slope_deg], s_list[slope_deg + 1],
                  a_list[asp_deg], a_list[asp_deg + 1], 1]
                list_condition[0] = h_list[height]
                list_condition[1] = h_list[height + 1]

                if list_condition[4] != 315:
                    list_condition[6] = 0
                conditions_matrix.append(list_condition)

    return conditions_matrix


def output_path_list (conditions_matrix, path, file_extension):
    """
    Creates a list containing the different output paths, that will be lately associated
      to each raster
    Parameters:
      conditions_matrix (numpy matrix): matrix containing the conditions for each raster
      path (string): common path for all the different output paths taht we'll generate
      file_extension (string): extension of the files that we will save
    Returns:
      conditions_output_path (list): list containing all the output paths for each raster
    """

    conditions_output_path = []

    for list_nb in enumerate(conditions_matrix):
        string = 'north'
        # Height:
        val_height_min = str(conditions_matrix[list_nb[0]][0])
        val_height_max = str(conditions_matrix[list_nb[0]][1])

        # Slope:
        val_slope_min = str(conditions_matrix[list_nb[0]][2])
        val_slope_max = str(conditions_matrix[list_nb[0]][3])

        # Aspect:
        val_aspect_min = conditions_matrix[list_nb[0]][4]
        val_aspect_max = conditions_matrix[list_nb[0]][5]

        if (val_aspect_min == 315 and val_height_max == 45):
            string = 'north'
        elif (val_aspect_min == 45 and val_aspect_max == 135):
            string = 'east'
        elif (val_aspect_min == 135 and val_aspect_max == 225):
            string = 'south'
        elif (val_aspect_min == 225 and val_aspect_max == 315):
            string = 'west'

        list_name = path + val_height_min + '_' + val_height_max + '_' + val_slope_min + '_' + val_slope_max + '_' + string + file_extension
        conditions_output_path.append(list_name)

    return conditions_output_path


def collect_paths (folder_path):
    """
    Creates a list containing the different output paths present on a folder
    Parameters:
      folder_path (string): path of the folder where the files are located
    Returns:
      list_paths (list): list containing all the paths of the files in the folder
    """

    list_paths = []

    for path in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, path)):
            list_paths.append(os.path.join(folder_path, path))

    return list_paths
