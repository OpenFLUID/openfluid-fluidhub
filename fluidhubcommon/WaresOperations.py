
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import json
import subprocess

from fluidhubcommon import ConfigManager
from fluidhubcommon import Constants


################################################################################
################################################################################


class WaresOperations :

  def __init__(self) :

    self.Config = ConfigManager.get()

    self.ReposRootDir = os.path.join(Constants.RootDataPath,self.Config["wareshub"]["gitserver"]["reposdir"])
    self.DefsRootDir = os.path.join(Constants.RootDataPath,self.Config["wareshub"]["gitserver"]["defsdir"])


################################################################################


  def getWareGitReposPath(self,Type,ID) :
    return os.path.join(self.ReposRootDir,Type,ID)


################################################################################


  def getWaresDefsPath(self,Type) :
    return os.path.join(self.DefsRootDir,Type)


################################################################################


  def getWareDefFilePath(self,Type,ID) :
    return os.path.join(self.getWaresDefsPath(Type),ID+".json")


################################################################################


  def getWareDefinition(self,Type,ID) :
    WareDefFile = self.getWareDefFilePath(Type,ID)

    if os.path.isfile(WareDefFile) :
      with open(WareDefFile) as DataFile :
        Data = json.load(DataFile)
        return Data

    return dict()


################################################################################


  def isUserGranted(self,Type,ID,Username,IsRW) :

    Data = self.getWareDefinition(Type,ID)

    if IsRW :
      if '*' in Data["users-rw"] :
        return True
      if Username in Data["users-rw"] :
        return True
    else :
      if '*' in Data["users-ro"] :
        return True
      if Username in Data["users-ro"] :
       return True
      if Username in Data["users-rw"] :
        return True

    return False


################################################################################


  def getMailingList(self,Type,ID) :

    Data = self.getWareDefinition(Type,ID)

    return Data["mailinglist"]


################################################################################


  def CreateWare(self,Type,ID,Definition) :

    WareGitPath = self.getWareGitReposPath(Type,ID)
    WareDefPath = self.getWaresDefsPath(Type)
    WareDefFile = self.getWareDefFilePath(Type,ID)

    if os.path.exists(WareGitPath) or os.path.isfile(WareDefFile) :
      return 409,"already exists"

    # check if provided json data is correct
    if not all(name in Definition for name in ("description","users-ro", "users-rw", "mailinglist")) :
      return 400,"invalid data provided"

    os.makedirs(WareGitPath)

    if not os.path.exists(WareDefPath) :
      os.makedirs(WareDefPath)

    # Initialization of the git repository
    P = subprocess.Popen(['git','init','--bare'],cwd=WareGitPath)
    P.wait()

    if P.returncode :
      return 500,"error while creating git repository"

    # Creation of the definitoin file
    with open(WareDefFile, 'w') as DefFile:
      Content = {"description" : Definition["description"],
                 "users-ro" : Definition["users-ro"],
                 "users-rw" : Definition["users-rw"],
                 "mailinglist" : Definition["mailinglist"]
                 }
      json.dump(Content, DefFile, indent=2)

    if not os.path.isfile(WareDefFile) :
      return 500,"error while creating definition file"

    return 200,""


################################################################################


  def GetWareInfo(self,Type,ID) :
    return 501,dict()
