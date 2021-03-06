
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import ConfigParser

from FluidHub import Constants


################################################################################
################################################################################


def __get():
  Filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"defaults.conf")
  LocalFilename = os.path.join(Constants.RootDataPath,Constants.CommonDataDir,"local.conf")

  Config = ConfigParser.ConfigParser()
  Config.read([Filename,LocalFilename])

  return Config


################################################################################
################################################################################


ConfigMan = __get()
