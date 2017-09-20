
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import errno


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
