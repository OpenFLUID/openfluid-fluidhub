
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest
import os
import shutil
from sh import git

from FluidHub import Tools

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_GitWaresOps(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.WaresUsers = {
      "sim.01" : "admin",
      "sim.02" : "admin",
      "sim.03" : "admin",
      "obs.01" : "admin",
      "obs.02" : "user2",
      "bext.01" : "admin"
    }


  def setUp(self):
    pass


################################################################################


  def getURL(self,Type,ID,User,Password):
    URL = "http://%s:%s@%s/wareshub/git/%s/%s" % (User,Password,helpers.FluidhubAddr,Type,ID)
    return URL


################################################################################


  def getLocalPath(self,Type,ID=None):
    if ID:
      return os.path.join(helpers.LocalWaresPath,Type,ID)
    else:
      return os.path.join(helpers.LocalWaresPath,Type)


################################################################################


  def test01_CloneWares(self):
    for Type, IDs in helpers.Wares.iteritems():
      TypePath = self.getLocalPath(Type)
      Tools.makedirs(TypePath)
      for ID in IDs:
        IDPath = self.getLocalPath(Type,ID)
        if os.path.exists(IDPath):
          shutil.rmtree(IDPath)
        Ret = git.clone(self.getURL(Type,ID,tests_GitWaresOps.WaresUsers[ID],tests_GitWaresOps.WaresUsers[ID]),_cwd=TypePath)
        self.assertEqual(Ret.exit_code,0)


################################################################################


  def test01_CommitPush(self) :
    WaresToCommitPush = { "simulators" : ["sim.01","sim.03"],
                          "observers" : ["obs.02"],
                          "builderexts" : ["bext.01"]
                        }
    for Type, IDs in WaresToCommitPush.iteritems():
      for ID in IDs:
        for Redo in range(0, 3):
          IDPath = self.getLocalPath(Type,ID)
          READMEPath = os.path.join(IDPath,"README.md")
          with open(READMEPath,'a') as RF:
            RF.write("Another line\n")
            Ret = git.add(READMEPath,_cwd=IDPath)
            self.assertEqual(Ret.exit_code,0)
            Ret = git.commit(m="Updated!",_cwd=IDPath)
            self.assertEqual(Ret.exit_code,0)
            Ret = git.branch("-m","openfluid-2.1",_cwd=IDPath)
            Ret = git.push("origin","openfluid-2.1",_cwd=IDPath)
            self.assertEqual(Ret.exit_code,0)


################################################################################

if __name__ == '__main__':
    unittest.main()
