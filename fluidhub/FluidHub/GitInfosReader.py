
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os

from FluidHub.WaresOperations import WaresOperations
from FluidHub.ConfigManager import ConfigMan  #REVIEW is this necessary?


################################################################################
################################################################################


class GitInfosReader() :

  def __init__(self,WareType,WareID,WareGitPath) :
    WaresOps = WaresOperations()
    self.WarePath = WareGitPath
    self.WaresHubDataPath = os.path.join(self.WarePath,"wareshub-data")


################################################################################


  def getGitStatsFile(self) :
    return os.path.join(self.WaresHubDataPath,"gitstats.json")


################################################################################


  def getGitBranchPath(self,Branch) :
    return os.path.join(self.WaresHubDataPath,Branch)


################################################################################


  def getGitBranchHistoryFile(self,Branch) :
    return os.path.join(self.getGitBranchPath(Branch),"commits-history.json")
