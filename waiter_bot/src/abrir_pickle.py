#!/usr/bin/env python3
import pickle
import pprint

obj = pickle.load(open("mapa_costa_coffee.pickle", "rb"))

with open("out.txt", "a") as f:
    pprint.pprint(obj, stream=f)