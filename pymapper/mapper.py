from functools import partial

import geopandas
import numpy
import pyproj
import cartopy.crs
import matplotlib.pyplot as plt
from pyproj import Transformer
from shapely.geometry import Point
from shapely.ops import transform

import matplotlib.tri as mtri
import pymapper.address_to_coordinate

ax = None
show_grid = False
def create_map():
    # creating global coordinate reference system variable so that it can be used from other functions
    global crs_in_projections
    crs_in_projections = "EPSG:3067"

    # loading a background map from shapefile
    background_map = geopandas.read_file("pymapper/shapefiles/maakunnat_siistitty.shp")

    # Create cartopy GeoAxes with proper projection
    etrs89 = cartopy.crs.epsg(3067)  # should be same as crs_in_projection
    global fig
    fig = plt.figure()
    global ax
    __add_wgs84_axis(visible_gridlines=show_grid)

    add_water_details_to_map()

    # plotting base map and adding details
    background_map.plot(ax= ax, color="white", edgecolor="black", alpha=0.2)
    # __add_coarse_water_details(ax)
    # __add_coarse_road_details(ax)


def show_map():
    plt.show()


def plot_triangles(latitudes, longitudes, values, colormap="winter", alpha=0.5, label=None):
    """
    Plots a contour on top of map
    :param latitudes: list of latitudes
    :param longitudes: list of longitudes
    :param values: list of z values
    :param colormap: colormap(optional)
    :param alpha: transparency(optional)
    :param label: color bar label(optional)
    :return:
    """

    # transforming coordinate points to etrs
    latitudes_fin = []
    longitudes_fin = []

    for i in range(len(latitudes)):
        lat, lon = __wgs_to_etrs(latitudes[i], longitudes[i])
        latitudes_fin.append(lat)
        longitudes_fin.append(lon)


    # triangulating etrs datapoints
    triang = mtri.Triangulation(latitudes_fin, longitudes_fin)

    # loading global ax and fig for plotting
    global ax
    global fig

    # Create a tricontour plot
    tricontour = ax.tricontourf(triang, values, cmap=colormap, alpha=alpha)

    # adding colorbar
    fig.colorbar(tricontour, ax=ax, label=label)




def plot_shapefile(filename, color="grey", edgecolor="grey", fill_transparency= 0.2):
    details2 = geopandas.read_file("pymapper/shapefiles/"+filename)
    details2 = details2.to_crs(crs_in_projections)
    details2.plot(ax=ax, color=color, edgecolor=edgecolor, alpha=fill_transparency)


def plot_point(latitude, longitude, color = "#FF8800", size = 10):
    """
    Adds a scatter point to plot
    :param latitude: in wgs84
    :param longitude: in wgs84
    :return: None
    """
    x, y = __wgs_to_etrs(latitude, longitude)
    plt.scatter(x, y, c= color, s = size)

def plot_address(address_string, color = "#7B68EE", size = 10):

    x, y = pymapper.address_to_coordinate.address_to_coordinate(address_string)
    print(x, y)
    plot_point(x, y, color=color)



def limit_map_to_region(top=61, bottom=59.9, left=23.5, right=26.5):

    global ax

    # projection, this is used to transform the points to the correct coordinate system

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3067")
    top, left = transformer.transform(top, left)
    bottom, right = transformer.transform(bottom, right)

    ax.set_xlim(left, right)
    ax.set_ylim(bottom, top)


def __add_wgs84_axis(visible_gridlines = False):
    global ax
    etrs89 = cartopy.crs.epsg(3067)  # should be same as crs_in_projection
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection=etrs89)
    ax.gridlines(draw_labels=True, visible=visible_gridlines)


def __wgs_to_etrs(latitude, longitude):

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3067")
    lat, lon = transformer.transform(latitude, longitude)

    return lat, lon


def add_title(title):
    plt.title(title)

def toggle_grid(on):
    global show_grid
    show_grid = on

def add_text_to_map(string, latitude, longitude, color="black"):
    x, y = __wgs_to_etrs(latitude, longitude)

    plt.text(x, y, s= string)


def add_water_details_to_map():
    global ax
    details1 = geopandas.read_file("pymapper/shapefiles/simplewaters.shp")
    details1 = details1.to_crs(crs_in_projections)
    details1.plot(ax=ax, color="lightskyblue")

def add__road_details():
    global ax
    details2 = geopandas.read_file("pymapper/shapefiles/mainroads.shp")
    details2 = details2.to_crs(crs_in_projections)
    details2.plot(ax=ax, color="grey", alpha=0.2)