
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os


################################################################################
################################################################################


ResourcesPath = os.path.dirname(os.path.abspath(__file__))
RootPath = os.path.dirname(ResourcesPath)
DataDevPath = os.path.join(RootPath,"_data-dev")

AccessToken = "Bjr0WBcPUiUNwubCX7Kbnnnjl2cq3LZArSbwqKBfNVCvhUxEm6CONukGU4DXoPlE"

Wares = { "simulators" : ["sim.01","sim.02","sim.03"],
          "observers" : ["obs.01","obs.02"],
          "builderexts" : ["bext.01"]
        }
