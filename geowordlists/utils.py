#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : utils.py
# Author             : Podalirius (@podalirius_)
# Date created       : 28 May 2023

import math


def haversine_distance(origin, destination):
    """
    Calculate the great-circle distance between two points on Earth using the haversine formula.

    Args:
        origin: Tuple of (latitude, longitude) coordinates for the starting point
        destination: Tuple of (latitude, longitude) coordinates for the ending point

    Returns:
        float: Distance between the points in kilometers, rounded to 2 decimal places

    The haversine formula determines the great-circle distance between two points on a sphere
    given their latitudes and longitudes. This implementation uses Earth's mean radius of
    6,371,009 meters and returns the distance in kilometers.
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    # Earth radius in meters
    radius = 6371009

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) * math.sin(dlat / 2) +
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
        math.sin(dlon / 2) * math.sin(dlon / 2)
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return round(d/1000, 2)


def size_in_bytes(size):
    """
    Convert a size in bytes to a human readable string with appropriate units.

    Args:
        size: Size in bytes as an integer

    Returns:
        str: Human readable string with size and units (e.g. "1.50 MB")
    """
    units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB']
    for k in range(len(units)):
        if size < (1024 ** (k + 1)):
            break
    return "%4.2f %s" % (round(size / (1024 ** (k)), 2), units[k])
