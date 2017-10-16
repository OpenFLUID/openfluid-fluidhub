
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import errno
import re


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
