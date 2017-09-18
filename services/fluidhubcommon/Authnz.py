
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os

from passlib.apache import HtpasswdFile

import Constants


################################################################################
################################################################################


def authenticateUser(username,password) :
  # TODO use SQLite with SQLAlchemy instead
  Filename = os.path.join(Constants.RootDataPath,Constants.CommonDataDir,"users.pass")
  ht = HtpasswdFile(Filename)
  return ht.check_password(username,password)
