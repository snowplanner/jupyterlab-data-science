# pylint: disable=unspecified-encoding, method-hidden
'''
Module containing functions to:
  - Load a geojson/shp file
  - Load a list with the geometries of a geojson/shp
  - Write into disk a geojson
'''

import json
import geojson
import geopandas as gpd
import fiona


def load_json_file (path_file_geojson):
    """
      Loads a geojson file
      Parameters:
        path_file_geojson (string): path where it is stored the geojson file
    """
    with open(path_file_geojson, 'r') as function:
        trails_json = json.loads(function.read())
    return trails_json


def load_geom_json (trails_geojson):
    """
      Loads the set of geometries of a geojson file
      Parameters:
        trails_geojson (geojson): json file loaded into python
    """
    trails_geom = [feature['geometry'] for feature in trails_geojson['features']]
    return trails_geom


def load_shapefile_geometries (shp_input_path):
    """ './outputs/shapefile_geojson/trails_2d_shapefile.shp'
      Loads the geometries of a shapefile
      Parameters:
        shp_input_path (string): path where it is stored the shp file
      Returns:
        shapes (dict): dictionary containing the different geometry objects stored in the shp file
    """
    with fiona.open(shp_input_path) as shapefile:
        shapes = [feature['geometry'] for feature in shapefile]
    return shapes


def write_geojson (input_file, output_path):
    """
      Saves the geojson as a file
      Parameters:
        input_file (geojson): json file loaded into python
        output_path (string): path where we will store the shapefile
    """
    with open(output_path, 'w') as function:
        geojson.dump(input_file, function)


def write_shp (input_path, output_path):
    """
      Saves a json file into shapefile format
      Parameters:
        input_path (string): path where it is stored the json file
        output_path (string): path where will be saved the file in shp format
    """
    json_geodataframe = gpd.read_file(input_path)
    json_geodataframe.to_file(output_path)
