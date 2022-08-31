# pylint: disable=consider-using-enumerate, method-hidden
'''
Module containing functions to:
  - Flat a point, linestring, polygon, multipolygon
  - Delete the Z coordinate of a geojson file
'''


def flat_point(point):
    """
      Deletes the z-coordinate of a point object
      Parameters:
        point (list): list of three elements defining the position of the point in the space
    """
    return point[:-1] if len(point) == 3 else point


def flat_linestring(linestring):
    """
      Creates a list of flattened points
      Parameters:
        linestring (list): list of points defining a linestring
      Returns:
        new_linestring (list): returns a linestring with their points being flattened
    """
    new_linestring = []
    for point in linestring:
        new_linestring.append(flat_point(point))
    return new_linestring


def flat_polygon(polygon):
    """
      Creates a list of flattened linestrings
      Parameters:
        polygon (list): list of linestrings defining a polygon
      Returns:
        new_polygon (list): returns a polygon with their linestrings being flattened
    """
    new_polygon = []
    for linestring in polygon:
        new_polygon.append(flat_linestring(linestring))
    return new_polygon


def flat_multipolygon(multipolygon):
    """
      Creates a list of flattened polygons
      Parameters:
        multipolygon (list): list of polygons defining a multipolygon
      Returns:
        new_multipolygon (list): returns a multipolygon with their polygons being flattened
    """
    new_multipolygon = []
    for polygon in multipolygon:
        new_multipolygon.append(flat_polygon(polygon))
    return new_multipolygon


def delete_z_coordinate (geojson_file):
    """
      Flattens a list of different geometry objects to two-dimensions
      Parameters:
        geojson_file (json): geojson file containing the description of the different geometries
      Returns:
        trails_json_2d (json): returns a geojson file where the geometries have been flattened
        to two-dimensions
    """

    two_dim_geom = geojson_file['features']
    for i in range(len(two_dim_geom)):
        geometry_coords = two_dim_geom[i]['geometry']['coordinates']
        coords_2d = flat_multipolygon(geometry_coords)
        two_dim_geom[i]['geometry']['coordinates'] = coords_2d
    #Define the geojson:
    trails_json_2d = geojson_file.copy()
    trails_json_2d['features'] = two_dim_geom
    return trails_json_2d
