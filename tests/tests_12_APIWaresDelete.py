
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import unittest

import TestsHelpers as helpers


################################################################################
################################################################################


class tests_APIWaresDelete(unittest.TestCase):

  @classmethod
  def setUpClass(cls):

    cls.Token = helpers.askForToken("admin","admin")


  def setUp(self):
    pass


################################################################################
################################################################################


  def deleteWare(self,Type,ID) :
    URL = "http://%s/api/wares/%s/%s" % (helpers.FluidhubAddr,Type,ID)
    Headers = {
       'content-type': "application/json",
       'authorization': "JWT %s" % self.Token
    }

    Response = helpers.executeDeleteRequest(URL, Headers=Headers)
    helpers.printResponse(Response)
    return Response


################################################################################
################################################################################


  def test01_DeleteWares(self):
    for Type, IDs in helpers.Wares.iteritems():
      for ID in IDs:
        Response = self.deleteWare(Type,ID)


################################################################################
################################################################################


if __name__ == '__main__':
    unittest.main()
