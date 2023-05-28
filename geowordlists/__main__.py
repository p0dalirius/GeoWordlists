#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : __main__.py
# Author             : Podalirius (@podalirius_)
# Date created       : 28 May 2023

import os
import argparse
from geowordlists.countries.france import France


VERSION = "1.0.1"


def parseArgs():
    print("GeoWordlists.py v%s - by @podalirius_\n" % VERSION)

    parser = argparse.ArgumentParser(description="")

    parser.add_argument("-v", "--verbose", default=False, action="store_true", help='Verbose mode. (default: False)')
    parser.add_argument("--debug", dest="debug", action="store_true", default=False, help="Debug mode.")

    parser.add_argument("-k", "--kilometers", required=False, default=50, type=int, help="Search radius in kilometers around the client city.")

    parser.add_argument("-o", "--output-file", required=False, default="wordlist.txt", help="Output file containing the generated wordlist.")

    # parser.add_argument("--country", dest="country", required=True, help="Select country.")
    parser.add_argument("-p", "--postal-code", dest="postal_code", required=True, help="Postal code of the client city.")

    return parser.parse_args()


def main():
    options = parseArgs()

    # if options.country.lower() == "france":
    #     pass

    country = France(debug=options.debug)

    client_city = country.select_client_city(options.postal_code)

    if client_city is not None:
        candidates = country.radius_search(client_city, search_distance=options.kilometers)

        wordlist = country.generate(candidates)

        print("[>] Generated %d passwords sorted by probability" % len(wordlist))
        options.output_file = os.path.abspath(options.output_file)
        basepath = os.path.dirname(options.output_file)
        filename = os.path.basename(options.output_file)
        if basepath not in [".", ""]:
            if not os.path.exists(basepath):
                os.makedirs(basepath)
            path_to_file = basepath + os.path.sep + filename
        else:
            path_to_file = filename
        f = open(path_to_file, "w")
        f.write("\n".join(wordlist) + "\n")
        f.close()
        print("[+] Written '%s' (%s bytes)" % (path_to_file, len("\n".join(wordlist))))

if __name__ == '__main__':
    main()