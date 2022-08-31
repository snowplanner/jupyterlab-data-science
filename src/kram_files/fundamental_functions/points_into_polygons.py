'''
  Module containing functions to:
    - Polygonize a raster already filtered
    - Filter points inside polygons
'''

from rasterio.features import shapes
import rasterio
import geopandas as gpd

def polygonize_raster (input_raster_path):
    """
      Polygonizes an input raster that has been previously classified
      Parameters:
            input_raster_path (string): path where it is stored the raster
      Returns:
            polygonized_raster (GeoDataFrame): the DataFrame containing the different polygons
            encapsuling the raster
    """
    mask = None
    with rasterio.Env():
        with rasterio.open(input_raster_path) as src:
            image = src.read(1) # first band
            results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v)
            in enumerate(
                shapes(image, mask=mask, transform=src.transform)))

    geoms = list(results)
    polygonized_raster  = gpd.GeoDataFrame.from_features(geoms, crs='epsg:4326')

    return polygonized_raster

def points_into_polys (input_polygons, input_points_path):
    """
      From a collection of points determines which of them are inside a collection of polygons
        Parameters:
          input_polygons (GeoDataFrame): file containing the collection of polygons
          input_points_path (string): path where it is stored the file containing the points that
          have to be filtered
        Returns:
          points_contained (GeoDataFrame): DataFrame with the points that are inside the area of
          the polygons
    """
    #Preparing the polyons:
    polygons = input_polygons.copy()
    polygons = polygons.loc[polygons.raster_val != 0.]

    #Loading the input_poitns:
    points = gpd.read_file(input_points_path)
    points = points.set_crs('epsg:4326')

    #Spatial Join:
    points_contained = gpd.sjoin(points, polygons, how='inner', predicate='within')
    points_contained.reset_index(inplace=True)

    return points_contained

def pretty_gdf (input_gdf):
    """
      Prepares the GeoDataFrame in order to be well-visualized:
        Parameters:
          input_gdf (GeoDataFrame)
        Returns:
          output_gdf (GeoDataFrame)
    """
    output_gdf = input_gdf.copy()
    output_gdf.drop(columns= ['index', 'lat', 'lon', 'raster_val'], inplace=True)
    output_gdf.rename(columns= {'index_right': 'polygon_nb'}, inplace=True)
    return output_gdf
