
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import errno
import re

from ConfigManager import ConfigMan


################################################################################
################################################################################


def makedirs(Path):
  try:
    os.makedirs(Path)
  except OSError as E:
    if E.errno == errno.EEXIST and os.path.isdir(Path):
      pass
    else:
      raise


################################################################################


def noneToEmptyString(Data):
  Ret = Data
  for Key in Ret:
    if Ret[Key] is None:
      Ret[Key] = ""

  return Ret


################################################################################


def isValidUsername(Username) :
  return re.match("^[a-z][a-z0-9]*$", Username)


################################################################################


def isValidEmail(Email) :
  return re.match("^[\w.\-_]*\@\w[\w.\-_]*$", Email)


################################################################################


def isValidEmail(Email) :
  return re.match("^[\w.\-_]*\@\w[\w.\-_]*$", Email)


################################################################################


def getAsValidList(Str,ValidFunc,WildcardOK=False,Sep=","):
  Lst = Str.split(Sep)
  ValidLst = list()

  for Item in Lst:
    Item = Item.strip(" ")

    if (WildcardOK and Item == "*") :
      ValidLst.append(Item)
    elif Item:
      if ValidFunc(Item):
        ValidLst.append(Item)
      else:
        return None

  return ValidLst


################################################################################


def getCurrentVersionGitBranch() :
  return "openfluid-"+ConfigMan.get("global","openfluid.currentversion","0.0")


################################################################################


def isOfficialGitBranch(Branch) :
  return re.match("^openfluid-\d+\.\d+(\.\d)?$", Branch)


################################################################################


def getVersionFromGitBranch(Branch) :
  if isOfficialGitBranch(Branch):
    return Branch[10:]
  return None


################################################################################


def getVersionsFromGitBranches(BranchesList) :
  Versions = list()
  for Branch in BranchesList:
    Ver = getVersionFromGitBranch(Branch)
    if Ver :
      Versions.append(Ver)

  #Versions.sort(cmp=lambda x, y: StrictVersion(x).__cmp__(y),reverse=True) # REVIEW use it instead?
  # from distutils.version import StrictVersion
  Versions.sort(reverse=True)
  return Versions
