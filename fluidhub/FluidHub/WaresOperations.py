
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import json
import subprocess
import shutil
import glob

from FluidHub.ConfigManager import ConfigMan
from FluidHub import Constants


################################################################################
################################################################################


class WaresOperations :

  def __init__(self) :

    self.ReposRootDir = os.path.join(Constants.RootDataPath,ConfigMan.get("wareshub","gitserver.reposdir"))
    self.DefsRootDir = os.path.join(Constants.RootDataPath,ConfigMan.get("wareshub","gitserver.defsdir"))


################################################################################


  # TODO check if these is useful and/or located in the right class
  @staticmethod
  def getGitCurrentVersionBranch() :
    return "openfluid-"+ConfigManager.get().get("global","openfluid.currentversion","0.0")


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


  def getWareGitURL(self,Type,ID,User=None) :

    UserAt = ""
    if User :
      UserAt = "%s@" % User

    PortColon = ""
    Port = ConfigMan.get("global","url-port","")
    if Port :
      PortColon = ":%s" % Port

    URL = [ ConfigMan.get("global","url-protocol"),"://",
            UserAt,ConfigMan.get("global","url-host"),PortColon,
            ConfigMan.get("global","url-prefix"),"/",
            ConfigMan.get("wareshub","url-prefix"),"/",
            ConfigMan.get("wareshub","gitserver.url-prefix"),"/",
            Type,"/",ID
          ]
    return "".join(URL)


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


  def createWare(self,Type,ID,Definition) :

    WareGitPath = self.getWareGitReposPath(Type,ID)
    WareDefPath = self.getWaresDefsPath(Type)
    WareDefFile = self.getWareDefFilePath(Type,ID)

    if os.path.exists(WareGitPath) or os.path.isfile(WareDefFile) :
      return 409,"already exists"

    # check if provided json data is correct
    if not all(name in Definition for name in ("shortdesc","users-ro", "users-rw", "mailinglist")) :
      return 400,"invalid data provided"

    os.makedirs(WareGitPath)

    if not os.path.exists(WareDefPath) :
      os.makedirs(WareDefPath)

    # Initialization of the git repository
    P = subprocess.Popen(['git','init','--bare'],cwd=WareGitPath)
    P.wait()

    # TODO setup of the default branch, and maybe default files?
    #
    #P = subprocess.Popen(["git","symbolic-ref","-q","HEAD","refs/heads/"+self.getGitCurrentVersionBranch()],
    #                     cwd=WareGitPath)
    #P.wait()

    if P.returncode :
      return 500,"error while creating git repository"

    # Creation of the definitoin file
    with open(WareDefFile, 'w') as DefFile:
      Content = {"shortdesc" : Definition["shortdesc"],
                 "users-ro" : Definition["users-ro"],
                 "users-rw" : Definition["users-rw"],
                 "mailinglist" : Definition["mailinglist"]
                 }
      json.dump(Content, DefFile, indent=2)

    if not os.path.isfile(WareDefFile) :
      return 500,"error while creating definition file"

    return 201,""


################################################################################


  def updateWare(self,Type,ID,Definition) :

    # TODO implement updating ware

    WareGitPath = self.getWareGitReposPath(Type,ID)
    WareDefPath = self.getWaresDefsPath(Type)
    WareDefFile = self.getWareDefFilePath(Type,ID)

    if not os.path.exists(WareGitPath) or not os.path.isfile(WareDefFile) :
      return 404,"does not exists"

    return 501,"not implemented"

    return 200,""


################################################################################


  def deleteWare(self,Type,ID) :

    WareGitPath = self.getWareGitReposPath(Type,ID)
    WareDefPath = self.getWaresDefsPath(Type)
    WareDefFile = self.getWareDefFilePath(Type,ID)

    if not os.path.exists(WareGitPath) and not os.path.isfile(WareDefFile) :
      return 404,"does not exists"

    if os.path.exists(WareGitPath) :
      shutil.rmtree(WareGitPath)

    if os.path.isfile(WareDefFile) :
      os.remove(WareDefFile)

    return 200,""


################################################################################


  def getWareInfo(self,Type,ID) :

    WareGitPath = self.getWareGitReposPath(Type,ID)
    WareDefPath = self.getWaresDefsPath(Type)
    WareDefFile = self.getWareDefFilePath(Type,ID)

    if not os.path.exists(WareGitPath) or not os.path.isfile(WareDefFile) :
      return 404,"does not exists"

    with open(WareDefFile, 'r') as DefFile:
      Data = json.load(DefFile)
      return 200,Data

    return 500,dict()


################################################################################


  def getWaresInfo(self,Type,Username=None) :
    Infos = dict()

    DefFiles = glob.glob(os.path.join(self.getWaresDefsPath(Type),"*.json"))
    for File in DefFiles :
      ID = os.path.splitext(os.path.basename(File))[0]
      WareGitPath = self.getWareGitReposPath(Type,ID)
      if os.path.exists(WareGitPath) :
        with open(File, 'r') as DefFile:
          Infos[ID] = json.load(DefFile)

      Infos[ID]["git-url"] = self.getWareGitURL(Type,ID,Username)

      GitStatsFilePath = os.path.join(WareGitPath,"wareshub-data","gitstats.json")
      if os.path.exists(GitStatsFilePath) :
        with open(GitStatsFilePath, 'r') as StatsFile:
          Stats = json.load(StatsFile)
          Infos[ID]["git-branches"] = Stats["branches"]
          Infos[ID]["open-issues"] = Stats["open-issues"]
      else :
        Infos[ID]["git-branches"] = list()
        Infos[ID]["open-issues"] = {"bugs": 0,"features": 0,"reviews": 0}

    return 200,Infos


################################################################################


  def getAllWaresInfo(self) :
    Infos = dict()

    for Type in Constants.WareTypes :
      Infos[Type] = list()

      DefFiles = glob.glob(os.path.join(self.getWaresDefsPath(Type),"*.json"))
      for File in DefFiles :
        ID = os.path.splitext(os.path.basename(File))[0]
        if os.path.exists(self.getWareGitReposPath(Type,ID)) :
          Infos[Type].append(ID)

    return 200,Infos
