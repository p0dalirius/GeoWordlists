#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : france.py
# Author             : Podalirius (@podalirius_)
# Date created       : 28 May 2023

import json
import os
import re
from geowordlists.utils import haversine_distance


class France(object):
    """
    A class representing geographical data and search functionality for cities in France.

    This class provides methods to:
    - Load and access French postal code and city data
    - Look up cities by postal code
    - Search for cities within a specified radius of a given city

    Attributes:
        data: A list of dictionaries containing city data loaded from laposte_hexasmal.json
        debug: Boolean flag to enable/disable debug output
    """

    def __init__(self, debug=False, novariant=False):
        super(France, self).__init__()
        self.data = self.__load_data()
        self.debug = debug
        self.novariant = novariant

    def __load_data(self):
        """

        :return:
        """

        relative_path = ["..", "data", "france", "laposte_hexasmal.json"]
        absolute_path = os.path.sep.join([os.path.dirname(__file__)] + relative_path)

        f = open(absolute_path, "r")
        data = json.loads(f.read())
        f.close()

        return data

    def select_client_city(self, postal_code):
        """

        :param postal_code:
        :return:
        """
        found_client_city = None
        for client_city in self.data:
            if client_city["fields"]["code_postal"] == postal_code:
                found_client_city = client_city
        if found_client_city is not None:
            lat = found_client_city["geometry"]["coordinates"]["latitude"]
            long = found_client_city["geometry"]["coordinates"]["longitude"]

            print("[>] Using client city in [%s:%s] at (%s, %s), FRANCE" % (
                found_client_city["fields"]["code_postal"],
                found_client_city["fields"]["nom_de_la_commune"],
                lat,
                long
            ))
        else:
            print("[!] Could not find city in FRANCE by postal code '%s'" % postal_code)
        return found_client_city

    def radius_search(self, client_city, search_distance):
        """
        Search for candidate cities in specified radius based on haversine distance

        :param client_city:
        :param search_distance:
        :return:
        """

        lat_1 = client_city["geometry"]["coordinates"]["latitude"]
        long_1 = client_city["geometry"]["coordinates"]["longitude"]

        candidates = []
        for candidate_city in self.data:
            lat_2 = candidate_city["geometry"]["coordinates"]["latitude"]
            long_2 = candidate_city["geometry"]["coordinates"]["longitude"]

            distance = haversine_distance((lat_1, long_1), (lat_2, long_2))
            if distance <= search_distance:
                if self.debug:
                    print("[debug] Selecting candidate at %5.2f km of [%s:%s] => [%s:%s]" % (
                            distance,
                            client_city["fields"]["code_postal"],
                            client_city["fields"]["nom_de_la_commune"],
                            candidate_city["fields"]["code_postal"],
                            candidate_city["fields"]["nom_de_la_commune"]
                        )
                    )
                candidates.append({
                    "distance": distance,
                    "commune": candidate_city
                })

        # Sort by distance
        candidates = list(sorted(candidates, key=lambda x:x["distance"]))

        return candidates

    def generate(self, candidates, novariants):
        """

        :param candidates:
        :return:
        """

        wordlist = []
        
        for data in candidates:
            commune_name = data["commune"]["fields"]["nom_de_la_commune"]
            commune_name = re.sub("[ ',-]", "", commune_name)

            # These are the hardcoded generation rules
            variants = [
                commune_name + data["commune"]["fields"]["code_postal"][:2],
                commune_name + data["commune"]["fields"]["code_postal"][:2] + "!",
                commune_name + data["commune"]["fields"]["code_postal"],
                commune_name + data["commune"]["fields"]["code_postal"] + "!"
            ]

            if novariant == False:
                for variant in variants:
                    if variant not in wordlist:
                        wordlist.append(variant)
            else:
                if commune_name not in wordlist:
                    wordlist.append(commune_name)

        return wordlist