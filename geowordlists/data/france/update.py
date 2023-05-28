#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : update.py
# Author             : Podalirius (@podalirius_)
# Date created       : 28 May 2023

import json
import sys
import requests


srcurl = "https://datanova.laposte.fr/explore/dataset/laposte_hexasmal/download?format=json&timezone=Europe/Berlin&use_labels_for_header=false"

def format_commune(commune_name):
  # Splitter
  buffer = ""
  commune_name_parts = []
  for element in commune_name.split(' '):
    if len(element) == 1:
      buffer = element + "'"
    else:
      part = (buffer + element).lower()
      # First letter in uppercase
      part = part[0].upper() + part[1:]
      commune_name_parts.append(part)
      buffer = ""
  return ' '.join(commune_name_parts)


if __name__ == '__main__':
    print("[+] Downloading 'laposte_hexasmal.json' ... ", end="")
    sys.stdout.flush()
    r = requests.get(srcurl)
    data = r.json()
    print("done.")

    # Normalize
    print("[+] Normalizing commune names in 'laposte_hexasmal.json' ... ", end="")
    sys.stdout.flush()
    for k in range(len(data)):
        data[k]["fields"]["nom_de_la_commune"] = format_commune(data[k]["fields"]["nom_de_la_commune"])
        lat, long = data[k]["geometry"]["coordinates"][::-1]
        data[k]["geometry"]["coordinates"] = {"latitude": lat, "longitude": long}
    print("done.")

    # Write new data
    print("[+] Writing 'laposte_hexasmal.json' ... ", end="")
    sys.stdout.flush()
    f = open("laposte_hexasmal.json", "w")
    f.write(json.dumps(data))
    f.close()
    print("done.")