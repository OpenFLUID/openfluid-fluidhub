
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os

import Constants


################################################################################
################################################################################


def get():
  Filename = os.path.join(Constants.RootDataPath,Constants.CommonDataDir,"access-token")
  with open(Filename) as DataFile:
    Data = DataFile.readline()
    Data = Data.strip(' \t\n\r')
    return Data
  return dict()
