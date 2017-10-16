
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import sys


################################################################################
################################################################################


CurrentPath = os.path.dirname(os.path.abspath(__file__))
RootPath = os.path.dirname(os.path.dirname(CurrentPath))
FluidHubPath = os.path.join(RootPath,"fluidhub")
sys.path.append(FluidHubPath)
