
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import json
import os


################################################################################
################################################################################


def get():
  Filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.json")
  with open(Filename) as DataFile:
    Data = json.load(DataFile)
    return Data
  return dict()
